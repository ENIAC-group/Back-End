from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
import utils.project_variables as project_variables 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["date_of_birth", "email" ,"gender","firstname" ,"lastname"  , "id"  , "phone_number" ] #, "phone_number"]

    def validate(self, attrs):
        return super().validate(attrs)


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        validators=[password_validation.validate_password],
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'date_of_birth', 'password1', 'password2'  , 'id' #  i do not know whether its needed or not
                    , 'gender' , 'firstname' , 'lastname' , 'phone_number') # , 'phone_number')
                    
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True},
        }
    
    def validate_email(self, value):
        user = User.objects.filter(email__iexact=value)
        if user.exists():
            user = user.first()
            if user.is_email_verified:
                raise serializers.ValidationError("Email already exists.")
            # if user.verification_tries_count >= project_variables.MAX_VERIFICATION_TRIES:
            #     raise serializers.ValidationError("You have reached the maximum number of registration tries.")
            if user.phone_number != self.initial_data.get('phone_number'):
                raise serializers.ValidationError("Email already exists.")
            
        return str.lower(value)
    
    # def validate_phone_number(self, attrs):
    #     print(attrs)
    #     return attrs
    
    def validate_password2(self, value):
        
        if value != self.initial_data.get('password1'):
            raise serializers.ValidationError('Passwords must match.')
        return value
    
    def validate_password1(self, value):
        if value != self.initial_data.get('password2'):
            raise serializers.ValidationError('Passwords must match.')
        password_validation.validate_password(value)
        return value


class ActivationConfirmSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=4, min_length=4)


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "user does not exist."})

        if user.is_email_verified:
            raise serializers.ValidationError({"detail": "user with this email is already verified."})

        attrs['user'] = user
        return attrs



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    verification_code = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError("New password and confirm password do not match.")
        try:
            validate_password(new_password)
        except serializers.ValidationError as validation_error:
            raise serializers.ValidationError({"new_password": validation_error})
        return attrs


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField(
        label=("Email"),
    )
    password = serializers.CharField(
        label=("password"),
        style={"input_type": "password"},
        write_only=True
    )

    token = serializers.CharField(
        label =("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email and password:
            email = self.validate_email(email)
            user = User.objects.get(email__iexact=email)

            if not user.check_password(password):
                msg = ('Incorrect password.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_email_verified:
                raise serializers.ValidationError({"detail": "User is not verified."})
            attrs['user'] = user
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        return attrs
    

    def validate_email(self, value):
        msg = ('Email does not exist.')
        user_exists = User.objects.filter(email__iexact=value).exists()

        if not user_exists:
            raise serializers.ValidationError(msg)

        return str.lower(value)
    

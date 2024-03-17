from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
import utils.project_variables as project_variables 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["date_of_birth", "email" ,"gender","firstname" ,"lastname"  , "id" ]


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        validators=[password_validation.validate_password],
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'date_of_birth', 'password1', 'password2'   # 'id',   i do not know whether its needed or not
                    , 'gender' , 'firstname' , 'lastname')
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True},
        }
    
    def validate_email(self, value):
        print("validate email")
        user = User.objects.filter(email__iexact=value)
        if user.exists():
            user = user.first()
            if user.is_email_verified:
                raise serializers.ValidationError("Email already exists.")
            if user.verification_tries_count >= project_variables.MAX_VERIFICATION_TRIES:
                raise serializers.ValidationError("You have reached the maximum number of registration tries.")
            if user.username != self.initial_data.get('username'):
                raise serializers.ValidationError("Email already exists.")
        return str.lower(value)
    
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
            raise serializers.ValidationError({"detail": "user is already verified."})

        attrs['user'] = user
        return attrs
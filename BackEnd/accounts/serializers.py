from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["date_of_birth", "email" ,"gender","firstname" ,"lastname"  , "id"  , "phone_number"]



class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField(
        label=_("Email"),
    )
    password = serializers.CharField(
        label=_("password"),
        style={"input_type": "password"},
        write_only=True
    )
    token = serializers.CharField(
        label =_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email and password:
            email = self.validate_email(email)
            user = User.objects.get(email__iexact=email)

            if not user.check_password(password):
                msg = _('Incorrect password.')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_email_verified:
                raise serializers.ValidationError({"detail": "User is not verified."})

            attrs['user'] = user
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        return attrs

    def validate_email(self, value):
        msg = _('Email does not exist.')
        user_exists = User.objects.filter(email__iexact=value).exists()

        if not user_exists:
            raise serializers.ValidationError(msg)

        return str.lower(value)
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["date_of_birth", "email" ,"gender","firstname" ,"lastname"  , "id" ]

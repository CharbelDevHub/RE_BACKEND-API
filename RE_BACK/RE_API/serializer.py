from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'last_login', 'is_superuser', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'date_joined', 'birthdate', 'middleName', 'brokerCode',
                  'phoneNumberCode', 'phoneNumber', 'profileImage', 'agency_id', 'specialization_id',
                  'userType_id']

class AgencySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Agency
        fields = '__all__'
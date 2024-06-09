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


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']  # Adjust fields as per your City model

class AgencySerializer(serializers.ModelSerializer):
    
    city_description = serializers.SerializerMethodField()
    
    class Meta: 
        model = Agency
        fields = ['id', 'fullName', 'arFullName', 'shortName', 'licenseCode', 'city', 'city_description', 'logo', 'address', 'image']
    
    def get_city_description(self, obj):
        return obj.city.name if obj.city else None
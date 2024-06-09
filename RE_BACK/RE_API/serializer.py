from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id','username', 'password' ,'last_login', 'is_superuser', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'date_joined', 'birthdate', 'middleName', 'brokerCode',
                  'phoneNumberCode', 'phoneNumber', 'profileImage', 'agency_id', 'specialization_id',
                  'userType_id']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


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

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'  # Adjust fields as necessary

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'  # Adjust fields as necessary
   

class PaymentSerializer(serializers.ModelSerializer):
    paymentType = PaymentTypeSerializer()
    
    class Meta:
        model = Payment
        fields = '__all__'  # Adjust fields as necessary
         
            
class ContractSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    buyer = UserSerializer()
    property = PropertySerializer()

    class Meta:
        model = Contract
        fields = '__all__'
        
        
class AgencyNewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Agency
        fields = ['fullName', 'arFullName', 'shortName', 'licenseCode', 'address']
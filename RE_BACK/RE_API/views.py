# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Agency, City, Property
from .serializer import  AgencyNewSerializer, CitySerializer, PropertySerializer
from .models import Agency, Contract, Payment, User
from .serializer import AgencySerializer, ContractSerializer, PaymentSerializer, UserLoginSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                user_serializer = UserSerializer(user) 
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'is_admin':user.is_superuser,
                    'user' : user_serializer.data,
                    'profile_image': user.profileImage.url
                    })
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgencyDetailsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        agency_id = request.data['id']
        agency = Agency.objects.get(id=agency_id)
        serializer = AgencySerializer(agency)
        return Response(serializer.data)
    
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user instance
            user.set_password(serializer.validated_data['password'])  # Hash the password
            user.save()  # Save the user again to update the hashed password
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgencyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        if pk:
            agency = get_object_or_404(Agency, pk=pk)
            serializer = AgencySerializer(agency)
            return Response(serializer.data)
        else:
            agencies = Agency.objects.all()
            serializer = AgencySerializer(agencies, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, pk):
        agency = get_object_or_404(Agency, pk=pk)
        agency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AgencyUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        agency_id = request.data.get('id')
        
        if agency_id is None:
            return Response({'error': 'Agency ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agency = Agency.objects.get(id=agency_id)
        except Agency.DoesNotExist:
            return Response({'error': 'Agency not found'}, status=status.HTTP_404_NOT_FOUND)
        
        for field, value in request.data.items():
            if field != 'id' and field != 'city':
                if hasattr(agency, field):
                    setattr(agency, field, value)
        agency.save()
        serializer = AgencySerializer(agency)
        if serializer:
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AgencyDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
        agency_id = request.data.get('id')
        
        if agency_id is None:
            return Response({'error': 'agency does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agency = Agency.objects.get(id=agency_id)
        except Agency.DoesNotExist:
            return Response({'error': 'Agency not found'}, status=status.HTTP_404_NOT_FOUND)
        
        agency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class AgencyCreateView(APIView):  
      permission_classes = [AllowAny]
      
      def post(self, request):                
        serializer = AgencyNewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request): 
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
    

class UpdateUserAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        user_id = request.data['id']
        user = User.objects.get(id=user_id)

        data = request.data
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'birthdate' in data:
            user.birthdate = data['birthdate']
        if 'phoneNumber' in data:
            user.phoneNumber = data['phoneNumber']
        
        user.save()
        return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)

class ContractGetAllView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        contract = Contract.objects.all()
        serializer = ContractSerializer(contract, many=True)
        return Response(serializer.data)

class GetContractPaymentsView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        contract_id = request.data.get('contract_id')
        if not contract_id:
            return Response({"error": "Contract ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        contract = get_object_or_404(Contract, id=contract_id)
        payments = Payment.objects.filter(contract=contract)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class PropertyListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        property = Property.objects.all()
        serializer = PropertySerializer(property, many=True)
        return Response(serializer.data)
    
class PropertyDeleteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        property_id = request.data['property_id']
        property = Property.objects.get(id=property_id)
        property.deleted = True
        property.save()
        return Response({})
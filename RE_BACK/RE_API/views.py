# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Agency, City
from .serializer import AgencySerializer, CitySerializer, UserLoginSerializer, UserSerializer
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

class AgencyView(APIView):
    # permission_classes = [IsAuthenticated]
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
        serializer = AgencySerializer(data=request.data)
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
    


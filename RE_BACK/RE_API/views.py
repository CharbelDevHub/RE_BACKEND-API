# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Agency
from .serializer import AgencySerializer, UserLoginSerializer, UserSerializer
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

    def put(self, request, pk):
        agency = get_object_or_404(Agency, pk=pk)
        serializer = AgencySerializer(agency, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        agency = get_object_or_404(Agency, pk=pk)
        agency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

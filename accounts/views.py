from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import LoginSerializer


# Create your views here.


class LoginView(APIView):
    @extend_schema(responses=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        password = serializer.data['password']
        print(username)

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)

            response = Response(
                    {"message": "success", "user_id": user.id, "name": user.username,
                     "access_token": str(refresh.access_token)}, status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(refresh))
            return response
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    serializer_class = None

    def post(self, request, *args, **kwargs):
        cookie = request.COOKIES.get('refresh_token')
        if cookie:
            response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token')
            token = RefreshToken(cookie)
            token.blacklist()

            return response
        else:
            return Response({'message': 'Logout failed'}, status=status.HTTP_404_NOT_FOUND)


class RefreshTokenView(APIView):
    serializer_class = None

    def post(self, request, *args, **kwargs):

        refresh_cookie = request.COOKIES.get('refresh_token')
        if refresh_cookie:
            refresh = RefreshToken(refresh_cookie)
            response = Response({'message': 'Refresh successful', 'access_token': str(refresh.access_token)},
                                status=status.HTTP_200_OK)
            return response
        else:
            return Response({'message': 'Refresh failed'}, status=status.HTTP_404_NOT_FOUND)
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    print("LoginSerializer")
    username = serializers.CharField()
    password = serializers.CharField()
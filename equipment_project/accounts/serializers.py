from tokenize import TokenError

from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.admin import CustomUser


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(username=obj["username"])
        return {"access": user.tokens()["access"], "refresh": user.tokens()["refresh"]}

    class Meta:
        model = CustomUser
        fields = ["username", "password", "tokens"]

    def validate(self, attrs):
        username = attrs.get("username", "")
        password = attrs.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Неверные данные для входа")
        if not user.is_active:
            raise AuthenticationFailed("Аккаунт заблокирован, обратитесь к администратору")

        return {"username": user.username, "tokens": user.tokens}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")

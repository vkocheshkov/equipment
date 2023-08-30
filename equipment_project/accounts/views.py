from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.serializers import LoginSerializer, LogoutSerializer


class LoginAPIView(generics.GenericAPIView):
    """
    Аутентификация клиентского подключения осуществляется по JWT токенам.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    """
    Если пользователь выходит из системы, то его refresh токен помешается в "blacklist"
    """

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

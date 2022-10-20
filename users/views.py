import coreschema
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema, coreapi
from rest_framework.views import APIView
from users.authentication import ExpiringTokenAuthentication
from .serializers import UserSerializer, RegisterSerializer, LoginSerialiser


class UserDetailAPI(APIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)

        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register users
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Overwrite ObtainAuthToken: new token is always created on login, change username required to False, email is used inn username field
class CreateToken(ObtainAuthToken):
    serializer_class = LoginSerialiser

    if coreapi.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=False,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        old_token = Token.objects.filter(user=user)
        if old_token:
            old_token.delete()
        token = Token.objects.create(user=user)
        return Response({'token': token.key})


class Logout(APIView):
    permission_classes = ()
    authentication_classes = ()

    # Get token key from auth headers and delete token from db
    def post(self, request, *args, **kwargs):
        token_str = request.META.get('HTTP_AUTHORIZATION', '');
        if token_str:
            # get token from token string. ex: 'Token 234567890987654345678' => '234567890987654345678'
            key = token_str.split(' ')[1] if len(token_str.split(' ')) == 2 else None
            if key:
                token = Token.objects.filter(key=key).first()
                if token:
                    token.delete()
                    return Response(status=204)
        raise AuthenticationFailed({"error": "Invalid Token"})

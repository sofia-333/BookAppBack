import coreschema
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status, response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema, coreapi
from rest_framework.views import APIView

from app import settings
from users.authentication import ExpiringTokenAuthentication
from utils.mailer import send_reset_password_email
from . import serializers
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer


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
    serializer_class = LoginSerializer

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


# Request for Password Reset Link
class ForgotPassword(generics.GenericAPIView):
    serializer_class = serializers.EmailSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"{settings.FRONT_END_URL}/forgot-password/?encoded_pk={encoded_pk}&token={token}"
            try:
                send_reset_password_email(email, reset_link)
                return response.Response(status=status.HTTP_200_OK)
            except:
                raise ValidationError({"non_field_errors": ["Could not send email"]})
        else:
            return response.Response(
                {"email": ["User with provided email doesn't exists"]},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Verify and Reset Password Token View.
class ResetPasswordAPI(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = ()
    authentication_classes = ()

    # Verify token and encoded_pk and then reset the password.
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        return response.Response(status=status.HTTP_200_OK)

from django.urls import path
from rest_framework import routers
from users.views import RegisterUserAPIView, CreateToken, Logout, ResetPasswordAPI, ForgotPassword
from users.views import UserDetailAPI

router = routers.DefaultRouter()

urlpatterns = [
                  path("forgot-password/", ForgotPassword.as_view(), name="request-password-reset"),
                  path("reset-password/<str:encoded_pk>/<str:token>/", ResetPasswordAPI.as_view(),
                       name="reset-password"),
                  path('create-token/', CreateToken.as_view()),
                  path('logout/', Logout.as_view()),
                  path('user/', UserDetailAPI.as_view()),
                  path('register/', RegisterUserAPIView.as_view()),
              ] + router.urls

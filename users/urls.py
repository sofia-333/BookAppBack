from django.urls import path
from rest_framework import routers
from users.views import RegisterUserAPIView, CreateToken, Logout
from users.views import UserDetailAPI

router = routers.DefaultRouter()

urlpatterns = [
                  path('create-token/', CreateToken.as_view()),
                  path('logout/', Logout.as_view()),
                  path('user/', UserDetailAPI.as_view()),
                  path('register/', RegisterUserAPIView.as_view()),
              ] + router.urls

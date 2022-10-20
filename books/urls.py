from django.urls import path

from books.views import GetBookAPIView

urlpatterns = [
    path('book/<isbn>', GetBookAPIView.as_view()),
]

import re

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.api import get_book_data
from books.models import Book
from books.serializers import BookSerializer
from users.authentication import ExpiringTokenAuthentication


def is_valid_isbn(isbn):
    pattern = '^(?:ISBN(?:-1[03])?:?●)?(?=[0-9X]{10}$|(?=(?:[0-9]+[-●]){3})[-●0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[-●]){4})[-●0-9]{17}$)(?:97[89][-●]?)?[0-9]{1,5}[-●]?[0-9]+[-●]?[0-9]+[-●]?[0-9X]$'
    if re.match(pattern, isbn):
        return True
    return False


class GetBookAPIView(APIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, isbn):
        if not is_valid_isbn(isbn):
            raise ValidationError({"isbn": "Wrong ISBN number provided."})
        book = Book.objects.filter(Q(isbn_10=isbn) | Q(isbn_13=isbn)).first()
        if book:
            print("Got book from database")
            serializer = BookSerializer(book)
            return Response(serializer.data)

        book = get_book_data(isbn)
        if book:
            serializer = BookSerializer(data=book)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            raise ValidationError({"non_field_errors": ["Could not find the book."]})

from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            'isbn_10',
            'isbn_13',
            'title',
            'authors',
            'number_of_pages',
            'publish_date',
            'publishers',
            'publish_places',
            'subjects',
            'subject_places',
            'subject_people',
            'notes',
            'links',
            'cover_url'
        ]

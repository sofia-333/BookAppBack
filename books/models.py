from django.db import models
from django.db.models import JSONField


class Book(models.Model):
    isbn_10 = models.CharField(max_length=10, null=True, blank=True)
    isbn_13 = models.CharField(max_length=13, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    authors = JSONField(null=True, blank=True)
    number_of_pages = models.CharField(max_length=10, null=True, blank=True)
    publishers = JSONField(null=True, blank=True)
    publish_places = JSONField(null=True, blank=True)
    publish_date = models.CharField(max_length=20, null=True, blank=True)
    subjects = JSONField(null=True, blank=True)
    subject_places = JSONField(null=True, blank=True)
    subject_people = JSONField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    links = models.JSONField(null=True, blank=True)
    cover_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "book"

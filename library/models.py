from __future__ import unicode_literals
from django.contrib.auth.models import  User
from books.helpers import SlugifyUniquely

from django.db import models


class Genre(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(blank=True)
    author = models.ForeignKey(User)
    genres = models.ManyToManyField(Genre)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = SlugifyUniquely(self.name[:40], self.__class__)
        super(Book, self).save(*args, **kwargs)






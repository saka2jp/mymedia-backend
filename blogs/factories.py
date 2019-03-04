from factory.django import DjangoModelFactory

from .models import Blog


class BlogFactory(DjangoModelFactory):
    class Meta:
        model = Blog

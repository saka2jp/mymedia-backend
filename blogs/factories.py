import factory
from factory.django import DjangoModelFactory

from .models import Blog


class BlogFactory(DjangoModelFactory):
    class Meta:
        model = Blog

    title = factory.Faker('title')
    url = factory.Faker('url')
    thumbnail = factory.Faker('thumbnail')
    start_dt = factory.Faker('start_dt')
    end_dt = factory.Faker('end_dt')
    is_public = factory.Faker('is_public')

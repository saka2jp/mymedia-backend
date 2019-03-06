from factory.django import DjangoModelFactory

from .models import Article


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

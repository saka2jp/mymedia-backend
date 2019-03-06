from django.urls import path

from .views import ArticleDetail, ArticleList

urlpatterns = [
    path('', ArticleList.as_view()),
    path('<int:pk>/', ArticleDetail.as_view()),
]

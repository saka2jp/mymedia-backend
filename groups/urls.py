from django.urls import path

from .views import GroupList

urlpatterns = [
    path('', GroupList.as_view()),
]

from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    thumbnail = models.URLField()
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

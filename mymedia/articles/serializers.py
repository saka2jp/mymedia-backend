from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'thumbnail', 'start_dt', 'end_dt', 'is_public', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

from rest_framework import serializers

from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'thumbnail', 'start_dt', 'end_dt', 'is_public', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

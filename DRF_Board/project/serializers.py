from .models import Blog
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    # view에서 넘긴 user 를 받아와서 user.nickname -> 작성자
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Blog
        fields = '__all__' 
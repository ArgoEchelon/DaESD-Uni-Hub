from rest_framework import serializers
from django.contrib.auth.models import User
from communities.models import Community
from events.models import Event
from posts.models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']

class CommunitySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'created_at', 'owner']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'start_time', 'end_time', 'created_at', 'organizer', 'community']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'community']
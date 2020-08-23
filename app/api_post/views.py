from django.shortcuts import render
from rest_framework import generics, viewsets, authentication, permissions, status
from core import custompermissions
from core.models import Post
from api_post import serializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        custompermissions.PostPermission
    )

    def perform_create(self, serializer):
        return serializer.save(postFrom=self.request.user)


class MyPostListView(generics.ListAPIView):
    """Retrieving my posts"""
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        custompermissions.PostPermission
    )

    def get_queryset(self):
        return self.queryset.filter(postFrom=self.request.user)


class FriendPostListView(generics.ListAPIView):
    """Retrieving friend posts"""
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        custompermissions.PostPermission
    )

    def get_queryset(self):
        friendId = (self.request.GET.get('friendId', 0))
        return self.queryset.filter(postFrom=friendId)

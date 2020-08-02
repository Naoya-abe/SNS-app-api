from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions, status
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

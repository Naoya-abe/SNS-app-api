from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import response
from api_dm import serializers
from core.models import Message


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permnission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        returnself.queryset.filter(sender=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete is not allowed method.'}
        return Response(response, status=status.HTTP_400_BADREQUEST)

    def pertial_update(self, request, *args, **kwargs):
        response = {'message': 'Patch is not allowed method.'}
        return Response(response, status=status.HTTP_400_BADREQUEST)


class InboxListView(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)

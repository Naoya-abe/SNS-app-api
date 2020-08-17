from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, viewsets, authentication, permissions, status
from rest_framework.exceptions import ValidationError
from api_user import serializers
from core import custompermissions
from core.models import FriendRequest


class UserViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custompermissions.UpdateOwnProfile,)


class FriendRequestViewSet(viewsets.ModelViewSet):
    """Handle creating and updating friend request"""
    queryset = FriendRequest.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Return only the data that is relevant to request user.
        return self.queryset.filter(Q(askTo=self.request.user) | Q(askFrom=self.request.user))

    def perform_create(self, serializer):
        # Automatically attaching the request user to askFrom
        try:
            serializer.save(askFrom=self.request.user)
        except:
            raise ValidationError("User can have only unique request")

    # def destroy(self, request, *args, **kwargs):
    #     # Disabling the destroy method
    #     response = {'message': 'Delete is not allowed !'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        # Disabling the partial_update method
        response = {'message': 'Patch is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MyProfileListView(generics.ListAPIView):
    """Retrieving my profile"""
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (custompermissions.UpdateOwnProfile,)

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

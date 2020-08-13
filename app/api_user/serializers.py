from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import FriendRequest


class UserSerializer(serializers.ModelSerializer):
    """Serialize a user object"""
    class Meta():
        model = get_user_model()
        fields = (
            'id', 'email', 'password',
            'displayName', 'avatar', 'about'
        )
        extra_kwargs = {
            'email': {
                'write_only': True,
            },
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'about': {
                'allow_blank': True,
            },
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = get_user_model().objects.create_user(**validated_data)
        # 新規作成した際にTokenを作成する
        Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta():
        model = FriendRequest
        fields = ('id', 'askFrom', 'askTo', 'approved')
        # ログインしているユーザを自動で割り当てる
        extra_kwargs = {'askFrom': {'read_only': True}, }

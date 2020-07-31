from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authen.models import Token
from core.models import Profile, FriendRequest


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password',)
        extra_kwargs={'password': {'write_only': True}, }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        # 新規作成した際にTokenを作成する
        Token.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    # 日付はフォーマットを指定して記入
    created_at = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'displayName', 'userPro', 'avatar', 'about')
        extra_kwargs = {'userPro': {'read_only': True}, }


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ('id', 'askFrom', 'askTo', 'approved')
        # ログインしているユーザを自動で割り当てる
        extra_kwargs = {'askFrom': {'read_only': True}, }
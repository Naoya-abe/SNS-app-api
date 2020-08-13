from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import Message, FriendRequest
from django.db.models import Q


class FriendsFilter(serializers.PrimaryKeyRelatedField):
    # Messageのデータをやり取りする際に、付随してこのクラスのデータもやり取りができる

    def get_queryset(self):
        request = self.context['request']
        # 自分に友達申請が来て、なおかつ承認している友達申請オブジェクトの一覧を取り出す
        friends = FriendRequest.objects.filter(
            Q(askTo=request.user) & Q(approved=True)
        )

        # 友人申請オブジェクトから「id」だけを抜き出したい
        list_friend = []
        for friend in friends:
            list_friend.append(friend.askFrom.id)

        # 抜き出した「id」を元にユーザのオブジェクトを取得
        queryset = get_user_model().objects.filter(id__in=list_friend)
        return queryset


class MessageSerializer(serializers.ModelSerializer):

    # 友達申請が承認されているユーザだけに送れるようにする
    receiver = FriendsFilter()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message')
        extra_kwargs = {'sender': {'read_only': True}, }

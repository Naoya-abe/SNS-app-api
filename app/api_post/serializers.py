from rest_framework import serializers
from core.models import Post, Profile
from api_user.serializers import ProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    postFrom = ProfileSerializer(read_only=True)
    postFromId = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)

    class Meta:
        model = Post
        fields = ('id', 'postFrom', 'postFromId','content')
        extra_kwargs = {'postFrom': {'read_only': True}, }

    def create(self,validated_data):
        validated_data['postFrom'] = validated_data.get('postFromId', None)
        if validated_data['postFrom'] is None:
            raise serializers.ValidationError("user not found.") 
        del validated_data['postFromId']
        return Post.objects.create(**validated_data)

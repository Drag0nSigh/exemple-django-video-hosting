from rest_framework import serializers

from video.models import Like, Video, VideoFile


class VideoListSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Video
        fields = ('id', 'owner', 'name', 'created_at', 'total_likes')


class VideoDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    quality = serializers.SerializerMethodField()

    @staticmethod
    def get_quality(obj):
        return [video_file.quality for video_file in obj.video_files.all()]

    class Meta:
        model = Video
        fields = ('owner', 'name', 'created_at', 'total_likes', 'quality')


class VideoIdsSerializer(serializers.Serializer):
    ids = serializers.ListSerializer(child=serializers.IntegerField())

    class Meta:
        model = Video
        fields = ('id',)


class UserLikesStatsSerializer(serializers.Serializer):
    username = serializers.CharField(source='email')
    likes_sum = serializers.IntegerField(allow_null=True)

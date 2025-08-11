from django.db.models import Q, Sum, Subquery, OuterRef
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import VideoListSerializer, VideoDetailSerializer, VideoIdsSerializer, UserLikesStatsSerializer
from api.permissions import LikePermission, VideoPermission, StaffOnlyPermission
from video.models import Like, Video

User = get_user_model()


class VideoViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [VideoPermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return VideoListSerializer
        elif self.action == 'ids':
            return VideoIdsSerializer
        return VideoDetailSerializer

    def get_queryset(self):
        queryset = Video.objects.all().order_by('id')
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return queryset.all()
        if user.is_authenticated:
            return queryset.filter(Q(is_published=True) | Q(owner=user))
        return queryset.filter(is_published=True)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[LikePermission])
    def likes(self, request, pk=None):
        video = self.get_object()
        user = request.user

        if request.method == 'POST':
            with transaction.atomic():
                video = Video.objects.select_for_update().get(pk=video.pk)
                if not video.is_published:
                    return Response(
                        {"detail": "Нельзя лайкнуть не опубликованное видер"}, status=status.HTTP_403_FORBIDDEN
                    )

                if Like.objects.filter(user=user, video=video).exists():
                    return Response({"detail": "Вы уже лайкали это видер"}, status=status.HTTP_400_BAD_REQUEST)

                Like.objects.create(user=user, video=video)
                video.total_likes += 1
                video.save()
                return Response({"detail": "Лайк добавлен"}, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            with transaction.atomic():
                video = Video.objects.select_for_update().get(pk=video.pk)
                if not video.is_published:
                    return Response(
                        {"detail": "Нельзя снять лайк у не опубликованного видео"}, status=status.HTTP_403_FORBIDDEN)

                like = Like.objects.filter(user=user, video=video).first()
                if not like:
                    return Response({"detail": "Вы не лайкали это видео"}, status=status.HTTP_404_NOT_FOUND)

                like.delete()
                video.total_likes -= 1
                video.save()
                return Response({"detail": "Лайк убран"}, status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[StaffOnlyPermission],
        pagination_class=None)
    def ids(self, request):
        video_ids = Video.objects.filter(is_published=True).values_list('id', flat=True).order_by('id')
        return Response({"ids": list(video_ids)})

    @action(detail=False,
            methods=['get'],
            permission_classes=[StaffOnlyPermission],
            url_path='statistics-subquery',
            pagination_class=None)
    @action(detail=False,
            methods=['get'],
            permission_classes=[StaffOnlyPermission],
            url_path='statistics-subquery',
            pagination_class=None)
    @action(detail=False,
            methods=['get'],
            permission_classes=[StaffOnlyPermission],
            url_path='statistics-subquery',
            pagination_class=None)
    def statistics_subquery(self, request):
        subquery = Subquery(
            Video.objects.filter(
                is_published=True,
                owner_id=OuterRef('pk')
            ).values('owner_id').annotate(
                likes_sum=Sum('total_likes')
            ).values('likes_sum')
        )

        users = User.objects.annotate(
            likes_sum=subquery
        ).filter(
            likes_sum__isnull=False
        ).values(
            'email', 'likes_sum'
        ).order_by('-likes_sum')

        return Response(UserLikesStatsSerializer(users, many=True).data)


    @action(detail=False,
            methods=['get'],
            permission_classes=[StaffOnlyPermission],
            url_path='statistics-group-by',
            pagination_class=None)
    def statistics_group_by(self, request):
        users = User.objects.filter(
            videos__is_published=True
        ).annotate(
            likes_sum=Sum('videos__total_likes')
        ).values('email', 'likes_sum').order_by('-likes_sum')
        return Response(UserLikesStatsSerializer(users, many=True).data)

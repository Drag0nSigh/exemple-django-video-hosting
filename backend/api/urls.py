from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    VideoViewSet,
)




app_name = 'api'

v1_routers = DefaultRouter()
v1_routers.register(r'videos', VideoViewSet, basename='videos')
# v1_routers.register(r'videos/(?P<video_id>\d+)/likes', ReviewViewSet, basename='likes',)



urlpatterns = [
    path('v1/', include(v1_routers.urls)),

]
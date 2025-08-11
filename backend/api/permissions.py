from rest_framework.permissions import BasePermission


class VideoPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        if request.user.is_authenticated:
            return obj.is_published or obj.owner == request.user
        return obj.is_published


class LikePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.is_published


class StaffOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        is_staff = request.user.is_authenticated and request.user.is_staff
        return is_staff

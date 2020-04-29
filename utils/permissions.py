from rest_framework import permissions

# from users.models import AccessToken
from utils.utils import get_access_token


# class IsLoggedInUserOrAdmin(permissions.BasePermission):
#     message = 'You must be login before this action'
#
#     def has_permission(self, request, view):
#         auth_token = get_access_token(request)
#         is_blacklist_token = AccessToken.check_blacklist(auth_token)
#         if is_blacklist_token:
#             return False
#         return bool(request.user or request.user.is_staff)
#
#     def has_object_permission(self, request, view, obj):
#         return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class IsNotBanUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_baned==False))

from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsPrincipal(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'principal'

class IsSquad(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'squad'

class IsPrincipalOrSquad(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['principal', 'squad']

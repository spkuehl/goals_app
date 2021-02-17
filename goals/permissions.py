from rest_framework.permissions import BasePermission
from .models import Goal, GoalLog


class IsAdminOrIsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        if type(obj) == GoalLog:
            return obj.goal.user == request.user or request.user.is_staff or request.user.is_superuser
        else:
            return obj.user == request.user or request.user.is_staff or request.user.is_superuser

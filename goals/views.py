from django.contrib.auth.models import User
from .models import Goal, GoalLog
from .permissions import IsAdminOrIsSelf
from .serializers import GoalSerializer, GoalLogSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class GoalViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows goals to be CRUDable.
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsSelf]

    def get_queryset(self):
        """
        This view should return a list of all the goals
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser:
            return Goal.objects.all()
        else:
            return Goal.objects.filter(user=user)

    @action(detail=True, url_path="goal-log-list")
    def goal_log_list(self, request, pk=None):
        goal = self.get_object()
        goal_logs = GoalLog.objects.filter(goal=goal)
        serialized_goal_logs = GoalLogSerializer(goal_logs, many=True)
        return Response(serialized_goal_logs.data)

    @action(detail=True, url_path="notification-list")
    def notification_list(self, request, pk=None):
        goal = self.get_object()
        notifications = Notification.objects.filter(goal=goal)
        serialized_notifications = NotificationSerializer(notifications, many=True)
        return Response(serialized_notifications.data)


class GoalLogViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows GoalLogs to be CRUDable
    """
    serializer_class = GoalLogSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsSelf]

    def get_queryset(self):
        """
        This view should return a list of all the goal logs
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser:
            return GoalLog.objects.filter(goal__user=user)
        else:
            return GoalLog.objects.filter(goal__user=user)

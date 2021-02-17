from django.contrib.auth.models import User
from .models import Goal, GoalLog
from .permissions import IsAdminOrIsSelf
from .serializers import GoalSerializer, GoalLogSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


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
        return Goal.objects.filter(user=user)


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
        return GoalLog.objects.filter(goal__user=user)

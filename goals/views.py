from django.contrib.auth.models import User
from .models import Goal, GoalLog
from .serializers import GoalSerializer
from rest_framework import viewsets
from rest_framework import permissions


class GoalViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows goals to be viewed or edited.
    """
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the goals
        for the currently authenticated user.
        """
        user = self.request.user
        return Goal.objects.filter(user=user)

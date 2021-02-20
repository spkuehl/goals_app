from django.contrib.auth.models import User
from .models import Notification
from goals.permissions import IsAdminOrIsSelf
from .serializers import NotificationSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class NotificationViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows notifications to be CRUDable.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrIsSelf]

    def get_queryset(self):
        """
        This view should return a list of all the notifications
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_superuser:
            return  Notification.objects.all()
        else:
            return Notification.objects.filter(user=user)

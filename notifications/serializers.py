from django.contrib.auth.models import User
from .models import Notification, FREQUENCY, DAY_OF_THE_WEEK

from rest_framework import fields, serializers


class NotificationSerializer(serializers.ModelSerializer):
    frequency = fields.MultipleChoiceField(choices=FREQUENCY)
    day_of_the_week = fields.MultipleChoiceField(choices=DAY_OF_THE_WEEK)

    class Meta:
        model = Notification
        fields = '__all__'

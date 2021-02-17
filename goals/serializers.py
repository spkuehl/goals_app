from django.contrib.auth.models import User
from .models import Goal, GoalLog, FREQUENCY

from rest_framework import fields, serializers


class GoalSerializer(serializers.ModelSerializer):
    check_in_frequency = fields.MultipleChoiceField(choices=FREQUENCY)
    reminder_frequency = fields.MultipleChoiceField(choices=FREQUENCY)

    class Meta:
        model = Goal
        fields = '__all__'


class GoalLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalLog
        fields = '__all__'

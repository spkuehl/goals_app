from django.contrib.auth.models import User
from .models import Goal, GoalLog

from rest_framework import fields, serializers


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'


class GoalLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalLog
        fields = '__all__'

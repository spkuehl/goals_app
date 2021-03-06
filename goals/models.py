from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    start_date = models.DateField(default=date.today, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_time = models.PositiveIntegerField(null=True, blank=True, help_text="Total time in hours, E.G. 10000 hours")
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}: {}'.format(self.user, self.name)

    @property
    def duration_completed(self):
        goal_logs = GoalLog.objects.filter(goal=self)
        duration = 0
        if goal_logs:
            for g in goal_logs:
                if g.duration:
                    duration = duration + g.duration
        return duration


class GoalLog(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    date_added = models.DateField(default=date.today, null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.goal, self.date_added)

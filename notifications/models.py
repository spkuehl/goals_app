from django.db import models
from django.contrib.auth.models import User
from goals.models import Goal
from multiselectfield import MultiSelectField


FREQUENCY = (
                ('daily', 'Daily'),
                ('weekly', 'Weekly'),
                ('monthly', 'Monthly'),
                ('quarterly', 'Quarterly'),
                ('half_yearly', 'Half Yearly'),
                ('yearly', 'Yearly')
            )

DAY_OF_THE_WEEK = (
                ('mon', 'Monday'),
                ('tues', 'Tuesday'),
                ('wed', 'Wednesday'),
                ('thurs', 'Thursday'),
                ('fri', 'Friday'),
                ('sat', 'Saturday'),
                ('sun', 'Sunday')
            )

NOTIFICATION_TYPE = (
                ('reminder', 'Reminder'),
                ('check_in', 'Check In')
            )

class Notification(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    frequency = MultiSelectField(choices=FREQUENCY, null=True, blank=True)
    day_of_the_week = MultiSelectField(choices=DAY_OF_THE_WEEK, null=True, blank=True)
    time_to_notify = models.TimeField(null=True, blank=True)
    type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{}: {}'.format(self.goal, self.active)

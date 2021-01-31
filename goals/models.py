from django.db import models
from django.contrib.auth.models import User
from datetime import date
from multiselectfield import MultiSelectField

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    start_date = models.DateField(default=date.today, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_time = models.PositiveIntegerField(null=True, blank=True)

    FREQUENCY = (('daily', 'Daily'),
                ('mon', 'Monday'),
                ('tues', 'Tuesday'),
                ('wed', 'Wednesday'),
                ('thurs', 'Thursday'),
                ('fri', 'Friday'),
                ('sat', 'Saturday'),
                ('sun', 'Sunday'),
                ('weekly', 'Weekly'),
                ('monthly', 'Monthly'),
                ('yearly', 'Yearly'))

    check_in_frequency = MultiSelectField(choices=FREQUENCY)
    reminder_frequency = MultiSelectField(choices=FREQUENCY)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}: {}'.format(self.user, self.name)

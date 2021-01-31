from django.contrib import admin
from .models import Goal, GoalLog

class GoalAdmin(admin.ModelAdmin):
    pass

admin.site.register(Goal, GoalAdmin)

class GoalLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(GoalLog, GoalLogAdmin)

from django.contrib import admin
from apps.core.models import Report, UserProfile, Campus

admin.site.register(Campus)
admin.site.register(Report)
admin.site.register(UserProfile)

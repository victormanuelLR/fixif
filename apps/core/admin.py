from django.contrib import admin
from apps.core.models import Report, UserProfile, Campus, CommentLike, ReportComment, ReportLike

admin.site.register(Campus)
admin.site.register(Report)
admin.site.register(UserProfile)
admin.site.register(ReportLike)
admin.site.register(ReportComment)
admin.site.register(CommentLike)
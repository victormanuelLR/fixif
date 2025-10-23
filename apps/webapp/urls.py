from django.urls import path
from apps.webapp.views import *

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('docs/', DocsView.as_view(), name='docs'),
    path('report', ReportView.as_view(), name="report"),

    path('api/report/<int:report_id>/like/', toggle_report_like, name='toggle_report_like'),
    path('api/comment/<int:comment_id>/like/', toggle_comment_like, name='toggle_comment_like'),
    path('api/report/<int:report_id>/comment/', create_comment, name='create_comment'),
    path('api/comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
]

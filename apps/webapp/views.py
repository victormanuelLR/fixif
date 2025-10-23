from django.views.generic.base import TemplateView 
from apps.core.models import UserProfile
from django.shortcuts import redirect
from apps.core.models import Report
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from apps.core.models import Report, ReportLike, ReportComment, CommentLike
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch, Q
from django.views.decorators.http import require_POST, require_http_methods


class IndexView(TemplateView):
    template_name = "webapp/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('webapp:feed')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeedView(TemplateView):
    template_name = "webapp/feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = UserProfile.objects.filter(user=self.request.user).first()
        if user_profile:
            context['user_profile'] = user_profile

        reports = Report.objects.filter(
            is_active=True
        ).annotate(
            like_count=Count('likes', filter=Q(likes__is_active=True)),
            comment_count=Count('comments', filter=Q(comments__is_active=True))
        ).prefetch_related(
            Prefetch(
                'comments',
                queryset=ReportComment.objects.filter(
                    is_active=True
                ).select_related('user').prefetch_related('likes')[:3], 
                to_attr='preview_comments'
            ),
            'likes'
        ).select_related('report_user').order_by('-created_at')

        if self.request.user.is_authenticated:
            user_liked_reports = set(
                ReportLike.objects.filter(
                    user=self.request.user,
                    is_active=True
                ).values_list('report_id', flat=True)
            )
            
            for report in reports:
                report.user_has_liked = report.id in user_liked_reports
                
                for comment in report.preview_comments:
                    comment.like_count = comment.likes.filter(is_active=True).count()
                    comment.user_has_liked = comment.likes.filter(
                        user=self.request.user,
                        is_active=True
                    ).exists()

        context['reports'] = reports

        context['stats'] = {
            'open': Report.objects.filter(is_active=True, report_status='OPEN').count(),
            'in_progress': Report.objects.filter(is_active=True, report_status='IN_PROGRESS').count(),
            'resolved': Report.objects.filter(is_active=True, report_status='RESOLVED').count(),
            'total': Report.objects.filter(is_active=True).count(),
        }

        return context


class ProfileView(TemplateView):
    template_name = "webapp/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = UserProfile.objects.filter(user=self.request.user).first()
        if user_profile:
            context['user_profile'] = user_profile

        return context


@login_required
@require_POST
def toggle_report_like(request, report_id):
    report = get_object_or_404(Report, id=report_id, is_active=True)
    
    existing_like = ReportLike.objects.filter(
        user=request.user,
        report=report
        ).first()

    if existing_like:
        
        if existing_like.is_active:
            existing_like.is_active = False
            existing_like.save()
            liked = False
        else:
            existing_like.is_active = True
            existing_like.save()
            liked = True

    else:
        ReportLike.objects.create(
            user=request.user,
            report=report
        )
        liked = True
    
    
    like_count = ReportLike.objects.filter(
        report=report,
        is_active=True
    ).count()
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'like_count': like_count
    })


@login_required
@require_POST
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(ReportComment, id=comment_id, is_active=True)
    
    existing_like = CommentLike.objects.filter(
        user=request.user,
        comment=comment,
        is_active=True
    ).first()
    
    if existing_like:
        existing_like.is_active = False
        existing_like.save()
        liked = False
    else:
        CommentLike.objects.create(
            user=request.user,
            comment=comment
        )
        liked = True
    
    like_count = CommentLike.objects.filter(
        comment=comment,
        is_active=True
    ).count()
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'like_count': like_count
    })


@login_required
@require_POST
def create_comment(request, report_id):
    import json
    
    report = get_object_or_404(Report, id=report_id, is_active=True)
    
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({
                'success': False,
                'error': 'Comentário não pode estar vazio'
            }, status=400)
        
        comment = ReportComment.objects.create(
            user=request.user,
            report=report,
            content=content
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'user_nickname': 'Você',
                'user_initial': 'R',
                'created_at': 'agora',
                'like_count': 0,
                'user_has_liked': False,
                'is_author': True
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(['DELETE', 'POST'])
def delete_comment(request, comment_id):
    comment = get_object_or_404(ReportComment, id=comment_id, is_active=True)
    
    if comment.user != request.user:
        return JsonResponse({
            'success': False,
            'error': 'Você não tem permissão para deletar este comentário'
        }, status=403)
    
    comment.is_active = False
    comment.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Comentário deletado com sucesso'
    })


class DocsView(TemplateView):
    template_name = "docs-template.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Campus(BaseModel):
    campus_name = models.CharField(max_length=160, verbose_name="Nome do Campus")


class UserProfile(BaseModel):
    campus = models.ForeignKey(
        Campus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Campus"
    )
    suap_username = models.CharField(max_length=50, unique=True, verbose_name="Enrollment Number")
    suap_avatar_url = models.URLField(max_length=500, blank=True, null=True)
    suap_nickname = models.CharField(max_length=100, blank=True, null=True)
    suap_full_name = models.CharField(max_length=200, blank=True, null=True)
    suap_course = models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
class Report(BaseModel):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Baixa'
        MEDIUM = 'MEDIUM', 'Média'
        HIGH = 'HIGH', 'Alta'


    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Aberto'
        IN_PROGRESS = 'IN_PROGRESS', 'Em andamento'
        RESOLVED = 'RESOLVED', 'Resolvido'
        CLOSED = 'CLOSED', 'Fechado'


    class ProblemType(models.TextChoices):
        NOT_INFORMED = 'NULL', 'Não Informado'
        HARDWARE = 'HARDWARE', 'Hardware'
        SOFTWARE = 'SOFTWARE', 'Software'
        NETWORK = 'NETWORK', 'Rede'
        ELECTRICAL = 'ELECTRICAL', 'Elétrica'
        CLIMATE = 'CLIMATE', 'Climatização'
        AUDIOVISUAL = 'AUDIOVISUAL', 'Audiovisual'
        FURNITURE = 'FURNITURE', 'Mobília'

    campus = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name="reports",
        verbose_name="Campus"
    )

    report_user = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='reports',
        verbose_name='Usuário que reportou'
    )

    is_anonim = models.BooleanField(default=False, verbose_name='Reportar Anonimamente')
    description = models.TextField(verbose_name='Descrição do Problema')

    priority = models.CharField(
        max_length=10, 
        choices=Priority.choices, 
        default=Priority.MEDIUM,
        verbose_name='Prioridade do Problema'
    )

    location = models.CharField(
        max_length=150, 
        verbose_name='Localização do Problema'
    )

    report_type = models.CharField(
        max_length=20, 
        choices=ProblemType.choices, 
        default=ProblemType.NOT_INFORMED,
        verbose_name="Tipo de Problema"
    )

    report_status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.OPEN,
        verbose_name="Status do Chamado"
    )

    assigned_to = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_reports",
        verbose_name="Responsável pelo Atendimento"
    )

    attachments = models.FileField(
        upload_to="reports/attachments/",
        null=True,
        blank=True,
        verbose_name="Anexo (opcional)"
    )

    resolved_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Data de Resolução"
    )

    def mark_as_resolved(self, user=None):
        self.report_status = self.Status.RESOLVED
        self.resolved_at = timezone.now()
        if user:
            self.assigned_to = user
        self.save()

    def __str__(self):
        return f"[{self.get_report_status_display()}] {self.location} - {self.description[:30]}"


class ReportLike(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="report_likes",
        verbose_name="Usuário"
    )
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="Relatório"
    )

    class Meta:
        unique_together = ('user', 'report')
        verbose_name = "Curtida em Relatório"
        verbose_name_plural = "Curtidas em Relatórios"

    def __str__(self):
        return f"{self.user.username} liked report #{self.report.id}"


class ReportComment(BaseModel):
    report = models.ForeignKey(
        "Report",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Relatório"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="report_comments",
        verbose_name="Usuário"
    )

    content = models.TextField(verbose_name="Comentário")
    is_anonim = models.BooleanField(default=False)
    
    attachment = models.FileField(
        upload_to="reports/comments/",
        null=True,
        blank=True,
        verbose_name="Anexo (opcional)"
    )

    class Meta:
        verbose_name = "Comentário em Relatório"
        verbose_name_plural = "Comentários em Relatórios"

    def __str__(self):
        return f"Comment by {self.user.username} on report #{self.report.id}"


class CommentLike(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_likes",
        verbose_name="Usuário"
    )
    comment = models.ForeignKey(
        ReportComment,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="Comentário"
    )

    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = "Curtida em Comentário"
        verbose_name_plural = "Curtidas em Comentários"

    def __str__(self):
        return f"{self.user.username} liked comment #{self.comment.id}"


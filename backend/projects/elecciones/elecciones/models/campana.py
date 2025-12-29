from django.db import models
from .....geografia.models.distrito import Distrito


class Campana(models.Model):
    """
    Campaña: candidato + distrito + ciclo (año/elección)
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    candidate = models.CharField(blank=True, null=True)
    district = models.ForeignKey(Distrito, on_delete=models.PROTECT, related_name='campaigns')
    cycle = models.CharField(max_length=50, help_text="Ej: 2025 - Elección General")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['district'], name='idx_campaign_district'),
        ]

    def __str__(self):
        return f"{self.name} ({self.cycle})"

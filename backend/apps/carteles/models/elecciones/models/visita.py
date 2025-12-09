from django.db import models
from .campana import Campana
from .colaborador import Colaborador
from .votante import Votante
from django.contrib.gis.db import models as gis_models

class Visit(models.Model):
    """
    Registro de cada visita. Se autoregistra fecha y ubicación (si la app la provee).
    - result: 1..5 (1 = rechazo, 5 = promesa de voto)
    - notes: texto libre
    - transport_needed: si requiere transporte para el día D
    """
    RESULT_CHOICES = [(i, str(i)) for i in range(1, 6)]

    id = models.BigAutoField(primary_key=True)
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, related_name='visits')
    colaborador = models.ForeignKey(Colaborador, on_delete=models.SET_NULL, null=True, related_name='visits')
    votante = models.ForeignKey(Votante, on_delete=models.PROTECT, related_name='visits')
    created_at = models.DateTimeField(auto_now_add=True)  # cuando se registró la visita
    location = gis_models.PointField(null=True, blank=True, srid=4326)  # ubicación de la visita
    result = models.PositiveSmallIntegerField(choices=RESULT_CHOICES)
    notes = models.TextField(null=True, blank=True)
    transport_needed = models.BooleanField(default=False)
    # metadata
    device_info = models.JSONField(null=True, blank=True)  # opcional: info del dispositivo
    synced = models.BooleanField(default=True)  # para offline sync scenarios

    class Meta:
        indexes = [
            models.Index(fields=['campaign', '-created_at'], name='idx_visit_campaign_date'),
            models.Index(fields=['padron_entry'], name='idx_visit_padron'),
            models.Index(fields=['collaborator'], name='idx_visit_collab'),
            models.Index(fields=['result'], name='idx_visit_result'),
            # GIST index for location must be added via a GIS migration - Django does that for PointField
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(result__gte=1, result__lte=5), name='check_visit_result_range'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Visita {self.id} - {self.votante} by {self.colaborador} ({self.result})"

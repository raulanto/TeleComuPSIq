from django.db import models


from ..models.Cita import Cita
from ..models.TimeStampedModel import TimeStampedModel

class URLCita(TimeStampedModel):
    proxima_cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='url_cita', blank=True,verbose_name='Cita url')
    url = models.URLField()


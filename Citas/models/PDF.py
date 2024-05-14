from django.db import models
from .TimeStampedModel import TimeStampedModel
from ..models.Cita import Cita


class PDF(models.Model):
    ACEPTADO = True
    RECHAZADO = False

    ESTADO_CHOICES = (
        (ACEPTADO, 'Aceptado'),
        (RECHAZADO, 'Rechazado'),
    )

    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    pdf_archivo = models.FileField(upload_to='autorizaciones/')
    estado = models.BooleanField(choices=ESTADO_CHOICES, default=False)

    def aceptar_pdf(self):
        # Esta función cambia el estado del PDF a "aceptado" (True)
        self.estado = True
        self.save()

    def rechazar_pdf(self):
        # Esta función cambia el estado del PDF a "rechazado" (False)
        self.estado = False
        self.save()

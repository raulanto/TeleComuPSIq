from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from ..models.Cita import Cita
from ..models.TimeStampedModel import TimeStampedModel
from Registro.models.Doctor import Doctor
class AtencionCita(TimeStampedModel):
    ATENDIDA = True
    DESANTENDIDA = False

    ESTADO_CHOICES = (
        (ATENDIDA, 'Cita Atendida'),
        (DESANTENDIDA, 'Cita no atendida'),
    )
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='atencion',blank=True)
    observacion_Subjetiva = CKEditor5Field(verbose_name='Subjetiva',default='')
    observacion_Objetiva = CKEditor5Field(verbose_name='Objetiva',default='')
    observacion_Analisis = CKEditor5Field(verbose_name='Análisis',default='')
    observacion_Plan = CKEditor5Field(verbose_name='Plan',default='')
    estado = models.BooleanField(choices=ESTADO_CHOICES, default=False)

    doctor_atendiendo = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f'Atención de Cita {self.cita.id}'
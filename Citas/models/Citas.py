from django.contrib.auth.models import User
from django.db import models
from .TimeStampedModel import TimeStampedModel
from Registro.models import Paciente, Doctor
from django.core.exceptions import ValidationError


class Cita(TimeStampedModel):
    ACEPTADO = True
    RECHAZADO = False

    ESTADO_CHOICES = (
        (ACEPTADO, 'Aceptado'),
        (RECHAZADO, 'Rechazado'),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.BooleanField(choices=ESTADO_CHOICES, default=False)

    def verificar_disponibilidad(self):
        # Excluye la cita actual si está presente
        citas_existentes = Cita.objects.exclude(pk=self.pk) if self.pk else Cita.objects.none()

        # Consulta para verificar si hay alguna cita programada para este doctor en esta fecha y hora
        citas_existente = citas_existentes.filter(doctor=self.doctor, fecha=self.fecha, hora=self.hora).exists()

        if citas_existente:
            raise ValidationError("El doctor ya tiene una cita programada para esta fecha y hora.")

    def aceptar_cita(self):
        # Esta función cambia el estado de la cita a "aceptada"

        self.estado = True
        self.save()

    def rechazar_cita(self):
        # Esta función cambia el estado de la cita a "rechazada"
        self.estado = False
        self.save()

    def save(self, *args, **kwargs):
        self.verificar_disponibilidad()  # Verificar disponibilidad al guardar la cita
        super().save(*args, **kwargs)  # Llamar al método save() del modelo base


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

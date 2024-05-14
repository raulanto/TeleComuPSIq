from django.contrib.auth.models import User
from django.db import models
from .TimeStampedModel import TimeStampedModel
from Registro.models import Paciente, Doctor,Trabajador
from django.core.exceptions import ValidationError


class Cita(TimeStampedModel):
    ACEPTADO = True
    RECHAZADO = False

    ESTADO_CHOICES = (
        (ACEPTADO, 'Aceptado'),
        (RECHAZADO, 'Rechazado'),
    )
    nombre=models.CharField(max_length=50,default='Cita')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.BooleanField(choices=ESTADO_CHOICES, default=False)

    def verificar_disponibilidad(self):
        # Excluye la cita actual si está presente
        citas_existentes = Cita.objects.exclude(pk=self.pk)

        # Verifica la disponibilidad del doctor
        cita_doctor = citas_existentes.filter(doctor=self.doctor, fecha=self.fecha, hora=self.hora).exists()
        if cita_doctor:
            raise ValidationError("El doctor ya tiene una cita programada para esta fecha y hora.")

        # Verifica la disponibilidad del paciente
        cita_paciente = citas_existentes.filter(paciente=self.paciente, fecha=self.fecha, hora=self.hora).exists()
        if cita_paciente:
            raise ValidationError("El paciente ya tiene una cita programada para esta fecha y hora.")
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

    def __str__(self):
        return self.nombre


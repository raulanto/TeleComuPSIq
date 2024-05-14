from django import forms
from django.core.exceptions import ValidationError
from ..models.Cita import Cita



class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        paciente = cleaned_data.get('paciente')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if doctor and paciente and fecha and hora:
            try:
                # Al editar, self.instance contendrá la cita actual.
                cita = Cita(
                    doctor=doctor,
                    paciente=paciente,
                    fecha=fecha,
                    hora=hora
                )
                # Asignar el pk de la instancia actual si existe
                if self.instance.pk:
                    cita.pk = self.instance.pk
                cita.verificar_disponibilidad()
            except ValidationError as e:
                # Añadir error al formulario en lugar de lanzar la excepción
                self.add_error(None, e.message)  # Esto añade un error no relacionado con un campo específico
        return cleaned_data
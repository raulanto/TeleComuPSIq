from ..models.AtenderCita import AtencionCita


def atender_cita(modeladmin, request, queryset):
    for cita in queryset:
        if not cita.estado:  # Solo si el estado de la cita es False (no atendida)
            cita.estado = True  # Cambiar el estado de la cita a "Atendida"
            cita.save()  # Guardar la cita actualizada
            # Crear una instancia en AtencionCita
            AtencionCita.objects.create(
                cita=cita,
                doctor_atendiendo=cita.doctor,
                estado=False  # Establecer el estado de la atención como "Atendida"
                # Puedes incluir más campos de acuerdo a tus necesidades aquí
            )


atender_cita.short_description = "Atender cita"
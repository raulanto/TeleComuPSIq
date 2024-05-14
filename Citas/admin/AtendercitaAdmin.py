from django.contrib import admin
from ..models.AtenderCita import AtencionCita


@admin.register(AtencionCita)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['cita', 'doctor_atendiendo','estado']

    fieldsets = [
        ('S', {
            'fields': [
                'observacion_Subjetiva',
            ],
        }),
        ('O', {
            'fields': [
                'observacion_Objetiva',
            ],
        }),
        ('A', {
            'fields': [
                'observacion_Analisis',
            ],
        }),
        ('P', {
            'fields': [
                'observacion_Plan',
            ],
        }),
    ]

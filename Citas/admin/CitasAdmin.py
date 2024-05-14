from django.contrib import admin
from ..models.Cita import Cita
from ..models.PDF import PDF
from ..models.AtenderCita import AtencionCita
from ..forms.Citaform import CitaForm
from ..models.URLCita import URLCita
from Registro.models.Trabajador import Trabajador
from Registro.models.Doctor import Doctor


class PDfInline(admin.StackedInline):
    model = PDF
    fieldsets = (
        ('Archivos', {
            'fields': ('pdf_archivo',)
        }),
    )


class UrlCitaInline(admin.StackedInline):
    model = URLCita
    fieldsets = (
        ('Archivos', {
            'fields': ('url',)
        }),
    )


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):  # Es una buena práctica nombrar la clase de Admin con el sufijo 'Admin'
    form = CitaForm
    list_display = ['id', 'paciente', 'fecha', 'hora', 'estado']
    list_editable = ['estado']
    fieldsets = (
        ('Cita', {
            'fields': ('doctor', 'paciente', 'fecha', 'hora', 'trabajador',)
        }),
    )
    inlines = [PDfInline, UrlCitaInline]
    actions = ['atender_cita']

    # Trer los datos solo del usuario
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Verificar si el usuario actual es un superadministrador
        if request.user.is_superuser:
            return qs

        try:
            # Intentar obtener el trabajador asociado al usuario actual
            trabajador = Trabajador.objects.get(usuario=request.user)
            # Obtener el ID del trabajador asociado al usuario actual
            trabajador_id = trabajador.id
        except Trabajador.DoesNotExist:
            # Si no hay trabajador asociado, verificar si el usuario es un doctor
            if hasattr(request.user, 'doctor'):
                # Si es un doctor, obtener el ID del doctor
                doctor_id = request.user.doctor.id
                # Filtrar las citas relacionadas con el doctor
                return qs.filter(doctor_id=doctor_id)
            else:
                # Si el usuario no tiene trabajador ni es doctor, devolver un queryset vacío
                return qs.none()

        # Filtrar las citas relacionadas con el doctor que tiene el trabajador deseado
        return qs.filter(doctor__trabajador__id=trabajador_id)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            if not request.user.is_superuser:
                try:
                    trabajador = Trabajador.objects.get(usuario=request.user)
                    kwargs["queryset"] = Doctor.objects.filter(id=trabajador.fk_doctor_id)
                except Trabajador.DoesNotExist:
                    kwargs["queryset"] = Doctor.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

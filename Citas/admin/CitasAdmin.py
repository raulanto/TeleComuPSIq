from django.contrib import admin
from ..models.Cita import Cita
from ..models.PDF import PDF

from ..forms.Citaform import CitaForm
from ..models.URLCita import URLCita
from Registro.models.Trabajador import Trabajador
from Registro.models.Doctor import Doctor
from ..actions.CtiaActions import atender_cita

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
    list_display = ['id', 'paciente', 'fecha', 'hora', 'estado','trabajador']
    list_editable = ['estado']
    fieldsets = (
        ('Cita', {
            'fields': ('doctor', 'paciente', 'fecha', 'hora',)
        }),
    )
    inlines = [PDfInline, UrlCitaInline]
    actions = [atender_cita]



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

    def save_model(self, request, obj, form, change):
        # Si el usuario que está realizando la solicitud es un trabajador
        if request.user.is_authenticated:
            try:
                # Intentar obtener el trabajador asociado al usuario
                trabajador = Trabajador.objects.get(usuario=request.user)
                obj.trabajador = trabajador
            except Trabajador.DoesNotExist:
                # Si no hay trabajador asociado al usuario, no hacer nada
                pass
        # Si el usuario que está realizando la solicitud es un superadministrador
        elif request.user.is_superuser:
            # Puedes manejar esta situación como desees, por ejemplo, dejando el campo trabajador en blanco
            pass

        super().save_model(request, obj, form, change)

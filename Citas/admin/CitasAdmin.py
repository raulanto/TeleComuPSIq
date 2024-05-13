from django.contrib import admin
from django import forms
from ..models.Citas import Cita, PDF
from django.urls import reverse
from django.utils.safestring import mark_safe
from file_resubmit.admin import AdminResubmitMixin
from file_resubmit.admin import AdminResubmitFileWidget


class PDfInline(admin.StackedInline):
    model = PDF


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        cita = Cita(
            doctor=cleaned_data.get('doctor'),
            fecha=cleaned_data.get('fecha'),
            hora=cleaned_data.get('hora')
        )
        cita.verificar_disponibilidad()  # Verifica la disponibilidad al validar el formulario
        return cleaned_data


@admin.register(Cita)
class CitaNameAdmin(admin.ModelAdmin):
    form = CitaForm
    list_display = ['id', 'paciente', 'fecha', 'hora', 'estado']
    fieldsets = (
        ('Cita', {
            'fields': ('doctor', 'paciente', 'fecha', 'hora', 'usuario', 'estado',)
        }),
    )
    inlines = [PDfInline]


class PageModelForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = '__all__'
        widgets = {
            'pdf_archivo': AdminResubmitFileWidget,
        }


@admin.register(PDF)
class PDFAdmin(AdminResubmitMixin, admin.ModelAdmin):
    form = PageModelForm
    list_display = ['id','pdf_archivo','estado']
    list_editable = ['estado']



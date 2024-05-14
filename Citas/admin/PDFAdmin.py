from django.contrib import admin
from django import forms
from ..models.PDF import  PDF
from file_resubmit.admin import AdminResubmitMixin
from file_resubmit.admin import AdminResubmitFileWidget


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



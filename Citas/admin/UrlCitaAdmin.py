from django.contrib import admin
from ..models.URLCita import URLCita

@admin.register(URLCita)
class ModelNameAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin
from ..models.AtenderCita import AtencionCita

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
import html2text
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
    actions = ['generar_pdf']

    def generar_pdf(self, request, queryset):
        # Creamos un documento PDF que contendrá las notas clínicas de las citas seleccionadas
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="notas_clinicas.pdf"'

        # Creamos un objeto SimpleDocTemplate
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Creamos una lista para almacenar las tablas de notas clínicas
        tables = []
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.bypass_tables = False
        for cita in queryset:
            # Convertimos el contenido HTML a texto plano
            subjetiva = h.handle(cita.observacion_Subjetiva)
            objetiva = h.handle(cita.observacion_Objetiva)
            analisis = h.handle(cita.observacion_Analisis)
            plan = h.handle(cita.observacion_Plan)

            # Creamos los datos de la tabla
            data = [
                ['Subjetiva', subjetiva],
                ['Objetiva', objetiva],
                ['Análisis', analisis],
                ['Plan', plan],
            ]

            # Creamos el estilo de la tabla
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])

            # Creamos la tabla
            table = Table(data)
            table.setStyle(style)

            # Agregamos la tabla a la lista
            tables.append(table)

        # Construimos el PDF con todas las tablas
        doc.build(tables)

        return response

    generar_pdf.short_description = "Generar PDF de notas clínicas"
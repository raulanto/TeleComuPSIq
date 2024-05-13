# Generated by Django 5.0.6 on 2024-05-13 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0003_alter_pdf_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='estado',
            field=models.BooleanField(choices=[('Aceptado', 'Aceptado'), ('Rechazado', 'Rechazado')], default=False),
        ),
    ]
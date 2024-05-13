# Generated by Django 5.0.6 on 2024-05-13 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EstadoCita',
        ),
        migrations.AlterField(
            model_name='pdf',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cita',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='EstadoPDF',
        ),
    ]
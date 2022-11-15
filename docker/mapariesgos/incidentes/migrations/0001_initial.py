# Generated by Django 3.2.15 on 2022-10-31 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=2, unique=True, verbose_name='Clave Estado')),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='nombre')),
                ('abrev', models.CharField(max_length=10, unique=True, verbose_name='abrev')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Incidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icono', models.ImageField(upload_to='', verbose_name='Ruta al icono')),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=3, verbose_name='Clave Municipio')),
                ('nombre', models.CharField(max_length=150, verbose_name='nombre')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='incidentes.estado')),
            ],
        ),
        migrations.CreateModel(
            name='Incidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.DecimalField(decimal_places=20, max_digits=50, verbose_name='latitud')),
                ('longitud', models.DecimalField(decimal_places=20, max_digits=50, verbose_name='longitud')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('municipio', models.ForeignKey(default=2400, on_delete=django.db.models.deletion.PROTECT, to='incidentes.municipio')),
                ('publicador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('tipo_incidente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='incidentes.tipo_incidente')),
            ],
        ),
    ]
# Generated by Django 4.1.5 on 2023-02-23 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Libre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('concepto', models.TextField()),
                ('notas', models.TextField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=16)),
            ],
            options={
                'verbose_name': 'Libre',
                'verbose_name_plural': 'Libres',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('marca', models.TextField()),
                ('modelo', models.TextField()),
                ('ajuste', models.TextField()),
                ('entrada_nominal', models.TextField()),
                ('caldera', models.BooleanField(default=0)),
                ('condicion', models.TextField()),
                ('prueba', models.TextField()),
                ('alcance_acreditado', models.BooleanField(default=1)),
                ('notas', models.TextField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=16)),
                ('mantenimiento', models.BooleanField()),
                ('tipo_mantenimiento', models.TextField()),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puesto', models.TextField()),
                ('departamento', models.TextField()),
                ('telefono', models.CharField(max_length=14)),
                ('direccion', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
            },
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('solicitud', models.IntegerField()),
                ('codigo', models.IntegerField()),
                ('fecha_entrega', models.IntegerField()),
                ('condiciones', models.TextField()),
                ('notas_especiales', models.TextField()),
                ('notas_internas', models.TextField()),
                ('urgente', models.BooleanField(default=0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.cliente')),
                ('cotizado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.empleado')),
            ],
            options={
                'verbose_name': 'Cotizacion',
                'verbose_name_plural': 'Cotizacions',
            },
        ),
    ]
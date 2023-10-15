# Generated by Django 4.2 on 2023-04-13 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_alter_empleado_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empleado',
            options={'permissions': [('ver_clientes', 'Ver Clientes'), ('ver_cotizaciones', 'Ver Cotizaciones'), ('ver_usuarios', 'Ver Usuarios'), ('ver_dashboard', 'Ver Dashboard')], 'verbose_name': 'Empleado', 'verbose_name_plural': 'Empleados'},
        ),
    ]
# Generated by Django 4.2 on 2023-04-20 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_alter_cotizacion_condiciones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='codigo',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='solicitud',
            field=models.CharField(max_length=15),
        ),
    ]

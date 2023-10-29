# Generated by Django 4.2.5 on 2023-10-28 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_ordentrabajo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordentrabajo',
            old_name='id_Product',
            new_name='id_Products',
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='estatus',
            field=models.IntegerField(choices=[(0, 'vigente'), (1, 'aceptada'), (2, 'rechazada')], default=0),
        ),
    ]

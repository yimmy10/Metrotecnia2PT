# Generated by Django 4.1.5 on 2023-03-17 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_servicioespecial_delete_libre_servicio_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='acreditado',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='agua',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='cambio_p_ajuste',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='id_valvula',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='servicio',
            name='mantto_correctivo',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='mantto_preventivo',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='n_serie',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='servicio',
            name='otro_servicio',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='p_ajuste_dc',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='p_hermeticidad',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='p_neumatica',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='servicio',
            name='vapor',
            field=models.BooleanField(default=0),
        ),
    ]
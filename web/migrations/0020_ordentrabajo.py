

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_servicio_valor_ajuste'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoOT', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('fecha', models.DateField()),
                ('declaraconf', models.BooleanField(default=0)),
                ('ordenCompra', models.IntegerField()),
                ('notas', models.CharField(max_length=255)),
                ('serie', models.CharField(max_length=255)),
                ('id_Product', models.CharField(max_length=255)),
                ('notas_especiales', models.CharField(max_length=255)),
                ('cotizacion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.cotizacion')),
            ],
            options={
                'verbose_name': 'OrdenTrabajo',
                'verbose_name_plural': 'OrdenTrabajos',
            },
        ),
    ]

# Generated by Django 3.0 on 2019-12-19 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('direcciones', '0001_initial'),
        ('ordenes', '0002_orden_orden_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='direccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='direcciones.Direccion'),
        ),
    ]
# Generated by Django 3.0 on 2019-12-18 15:00

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
            name='Direccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(max_length=200)),
                ('line2', models.CharField(blank=True, max_length=200)),
                ('ciudad', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=100)),
                ('pais', models.CharField(max_length=50)),
                ('referencia', models.CharField(max_length=300)),
                ('codigo_postal', models.CharField(max_length=10)),
                ('default', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
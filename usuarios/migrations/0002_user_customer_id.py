# Generated by Django 3.0 on 2019-12-26 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='customer_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
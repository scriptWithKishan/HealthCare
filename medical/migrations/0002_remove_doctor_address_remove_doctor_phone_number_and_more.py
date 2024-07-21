# Generated by Django 5.0.3 on 2024-07-21 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='address',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='address',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.CharField(default='General', max_length=255),
        ),
    ]

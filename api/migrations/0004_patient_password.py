# Generated by Django 5.1.4 on 2024-12-28 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_idadministratifstaff_administratifstaff_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
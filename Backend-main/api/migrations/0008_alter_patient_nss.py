# Generated by Django 5.1.4 on 2024-12-29 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_ehr_administratifstaff_ehr_creator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='NSS',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

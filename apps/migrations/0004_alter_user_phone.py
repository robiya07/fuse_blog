# Generated by Django 4.1.3 on 2022-12-09 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
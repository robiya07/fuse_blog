# Generated by Django 4.1.3 on 2022-12-10 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='social',
            field=models.JSONField(default={'instagram': 'instagram.com'}),
            preserve_default=False,
        ),
    ]
# Generated by Django 5.0.6 on 2024-05-26 14:03

import sorl.thumbnail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=sorl.thumbnail.fields.ImageField(default=1, upload_to='profiles'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-28 15:34

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='media/default.jpg', upload_to=blog.models.save_image),
        ),
    ]

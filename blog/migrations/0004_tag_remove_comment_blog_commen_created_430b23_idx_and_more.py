# Generated by Django 4.2.5 on 2023-09-26 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_comment_blog_commen_created_79f39f_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('slug', models.SlugField(blank=True, max_length=25, null=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RemoveIndex(
            model_name='comment',
            name='blog_commen_created_430b23_idx',
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-created', 'post', 'active'], name='blog_commen_created_9a0cbb_idx'),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='blog_tag_name_43b6ed_idx'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='blog.tag'),
        ),
    ]
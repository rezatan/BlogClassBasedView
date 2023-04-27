# Generated by Django 4.1.6 on 2023-04-25 07:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='published',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
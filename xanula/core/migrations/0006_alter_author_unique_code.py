# Generated by Django 5.1 on 2024-08-22 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_author_unique_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='unique_code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

# Generated by Django 4.2 on 2023-05-02 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales',
            field=models.IntegerField(default=0),
        ),
    ]
# Generated by Django 4.2.3 on 2024-09-07 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='descripcion',
            field=models.TextField(),
        ),
    ]

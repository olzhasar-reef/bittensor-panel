# Generated by Django 4.2.11 on 2024-05-04 22:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hyperparameter",
            name="value",
            field=models.BigIntegerField(),
        ),
    ]
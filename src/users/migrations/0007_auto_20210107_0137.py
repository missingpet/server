# Generated by Django 3.1.3 on 2021-01-07 01:37
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_auto_20210105_1904"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ("-email",),
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]

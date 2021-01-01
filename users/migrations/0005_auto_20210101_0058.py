# Generated by Django 3.1.3 on 2021-01-01 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201126_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(
                db_index=True, max_length=254, unique=True, verbose_name='Адрес электронной почты'),
        ),
    ]

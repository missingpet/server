# Generated by Django 3.1.3 on 2020-11-26 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0009_auto_20201117_1020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={'ordering': ('-created_at',), 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
    ]
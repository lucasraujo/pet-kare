# Generated by Django 4.2 on 2023-04-03 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_alter_group_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='created_at',
            field=models.DateTimeField(auto_created=True, auto_now=True),
        ),
    ]
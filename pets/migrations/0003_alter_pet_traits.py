# Generated by Django 4.2 on 2023-04-03 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traits', '0001_initial'),
        ('pets', '0002_alter_pet_traits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='traits',
            field=models.ManyToManyField(related_name='pets', to='traits.trait'),
        ),
    ]

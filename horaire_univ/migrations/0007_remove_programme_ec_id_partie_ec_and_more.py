# Generated by Django 5.0.6 on 2024-08-27 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horaire_univ', '0006_remove_programme_ec_date_debut_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programme_ec',
            name='id_partie_ec',
        ),
        migrations.AlterField(
            model_name='partie_ec',
            name='date_debut',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='partie_ec',
            name='date_fin',
            field=models.DateField(),
        ),
    ]

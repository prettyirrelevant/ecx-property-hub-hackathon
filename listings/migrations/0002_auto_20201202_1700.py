# Generated by Django 3.1.3 on 2020-12-02 17:00
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
    ]

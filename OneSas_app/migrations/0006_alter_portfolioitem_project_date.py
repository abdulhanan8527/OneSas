# Generated by Django 5.1.7 on 2025-03-26 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OneSas_app', '0005_portfolioitem_client_portfolioitem_project_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioitem',
            name='project_date',
            field=models.DateField(),
        ),
    ]

# Generated by Django 3.1 on 2020-08-18 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_ticket_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default='Assigned', max_length=20),
        ),
    ]

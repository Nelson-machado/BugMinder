# Generated by Django 3.1 on 2020-08-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_ticketcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

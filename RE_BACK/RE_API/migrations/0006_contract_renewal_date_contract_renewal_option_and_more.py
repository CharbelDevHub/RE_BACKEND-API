# Generated by Django 4.2.11 on 2024-04-07 06:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RE_API', '0005_contract_expirydate_alter_payment_paymentdate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='renewal_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='renewal_option',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='termination_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='expiryDate',
            field=models.DateField(default=datetime.datetime(2024, 4, 7, 6, 38, 12, 44618, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paymentDate',
            field=models.DateField(default=datetime.datetime(2024, 4, 7, 6, 38, 12, 46644, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='request',
            name='issuedOn',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 7, 6, 38, 12, 46644, tzinfo=datetime.timezone.utc)),
        ),
    ]

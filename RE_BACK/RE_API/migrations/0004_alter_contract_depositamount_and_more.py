# Generated by Django 4.2.11 on 2024-04-06 19:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RE_API', '0003_rename_contact_transaction_contract_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='depositAmount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paymentDate',
            field=models.DateField(default=datetime.datetime(2024, 4, 6, 19, 34, 35, 311787, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='request',
            name='issuedOn',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 6, 19, 34, 35, 311787, tzinfo=datetime.timezone.utc)),
        ),
    ]

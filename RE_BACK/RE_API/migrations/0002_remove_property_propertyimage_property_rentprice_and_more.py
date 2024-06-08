# Generated by Django 4.2.11 on 2024-04-05 19:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RE_API', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='propertyImage',
        ),
        migrations.AddField(
            model_name='property',
            name='rentPrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='salePrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='issuedOn',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 5, 19, 20, 57, 344737, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/properties/')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='RE_API.property')),
            ],
        ),
    ]

# Generated by Django 2.2.17 on 2021-02-25 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20210224_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='customer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donation_customer_id', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.2.12 on 2023-06-08 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_orderitem_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Deliveryagent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.deliveryagent'),
        ),
    ]

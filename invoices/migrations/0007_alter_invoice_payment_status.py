# Generated by Django 5.0.7 on 2024-08-09 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_alter_invoice_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Due', 'Due')], default='Paid', max_length=20),
        ),
    ]

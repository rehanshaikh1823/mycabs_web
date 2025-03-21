# Generated by Django 5.0.7 on 2024-08-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_alter_invoice_invoice_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='status',
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment_status',
            field=models.CharField(choices=[('PAID', 'Paid'), ('Due', 'Due')], default='PAID', max_length=20),
        ),
    ]

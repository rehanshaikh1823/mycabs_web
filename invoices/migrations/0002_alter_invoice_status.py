# Generated by Django 5.0.7 on 2024-08-02 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('PAID', 'Paid')], default='PAID', max_length=20),
        ),
    ]

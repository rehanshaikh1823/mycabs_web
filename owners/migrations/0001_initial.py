# Generated by Django 5.0.7 on 2024-07-20 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=255)),
                ('business_address', models.TextField()),
                ('registration_number', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]

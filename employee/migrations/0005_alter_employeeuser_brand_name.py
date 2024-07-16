# Generated by Django 4.0.3 on 2024-07-13 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mybrand', '0001_initial'),
        ('employee', '0004_employeeuser_brand_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeuser',
            name='brand_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mybrand.brand'),
        ),
    ]

# Generated by Django 4.1.1 on 2022-10-07 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='refund_granted',
        ),
        migrations.RemoveField(
            model_name='order',
            name='refund_requested',
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='small_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

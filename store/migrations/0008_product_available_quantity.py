# Generated by Django 4.1.1 on 2022-11-24 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_count_sold_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_quantity',
            field=models.IntegerField(default=0, verbose_name='available quantity'),
        ),
    ]
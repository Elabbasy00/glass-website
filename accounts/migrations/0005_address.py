# Generated by Django 4.1.1 on 2022-11-22 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_verified_user_verification_numbers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100)),
                ('apartment_address', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=100)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
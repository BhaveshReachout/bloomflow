# Generated by Django 3.2 on 2022-05-03 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_order_orderdetails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='made_by',
        ),
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='checksum',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]

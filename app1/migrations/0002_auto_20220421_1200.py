# Generated by Django 3.2 on 2022-04-21 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_stamp', models.DateTimeField(auto_now=True)),
                ('is_order', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('C_name', models.CharField(max_length=35)),
                ('C_disc', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_mode', models.CharField(choices=[('cod', 'cod'), ('paytm', 'paytm')], default='cod', max_length=255)),
                ('ostatus', models.CharField(choices=[('created', 'Created'), ('shipped', 'Shipped'), ('paid', 'Paid')], default='created', max_length=255)),
                ('ocontactno', models.CharField(default='1', max_length=10)),
                ('oaddress', models.CharField(blank=True, max_length=255)),
                ('odate', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, to='app1.cartadd')),
                ('user', models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pname', models.CharField(max_length=100)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='')),
                ('Pcolour', models.CharField(max_length=50)),
                ('PCImage', models.ImageField(blank=True, null=True, upload_to='')),
                ('Pprice', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
                ('Pquantity', models.IntegerField(default=0)),
                ('Pdesc', models.CharField(max_length=255)),
                ('Psize', models.CharField(max_length=255)),
                ('Plight', models.CharField(max_length=255)),
                ('Pdifficulty', models.CharField(max_length=255)),
                ('PAirCleaner', models.CharField(max_length=255)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.category')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oquant', models.IntegerField(default=1)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app1.order')),
                ('product', models.ManyToManyField(to='app1.Product')),
            ],
            options={
                'db_table': 'orderdetails',
            },
        ),
        migrations.CreateModel(
            name='ItemRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rnumber', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modefied', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'itemrating',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=25)),
                ('l_name', models.CharField(max_length=25)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=10)),
                ('msg', models.TextField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'contact',
            },
        ),
        migrations.AddField(
            model_name='cartadd',
            name='product',
            field=models.ManyToManyField(blank=True, to='app1.Product'),
        ),
        migrations.AddField(
            model_name='cartadd',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

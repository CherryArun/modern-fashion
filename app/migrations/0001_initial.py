# Generated by Django 4.1.6 on 2023-03-01 11:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=2000)),
                ('image', models.FileField(null=True, upload_to='product/', verbose_name='Product Image')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('staff_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=40)),
                ('mail', models.EmailField(max_length=30)),
                ('mobile', models.CharField(max_length=15)),
                ('gender', models.CharField(choices=[('', 'Select'), ('male', 'Male'), ('female', 'Female')], max_length=30)),
                ('DOB', models.DateField()),
                ('DOJ', models.DateField()),
                ('designation', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=30)),
                ('address', models.TextField(max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('password', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=30)),
                ('pincode', models.CharField(max_length=10)),
                ('address', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_stock', models.CharField(max_length=500)),
                ('pruchased_product', models.CharField(max_length=500)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product_category'),
        ),
        migrations.CreateModel(
            name='Cart_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=50)),
                ('tot', models.IntegerField()),
                ('tot_price', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.datetime(2023, 3, 1, 11, 55, 6, 225774, tzinfo=datetime.timezone.utc))),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user_detail')),
            ],
        ),
    ]
# Generated by Django 4.0.3 on 2022-06-01 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(default=1)),
                ('name', models.CharField(max_length=300, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('serial', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('in_date', models.DateField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('amount', models.IntegerField(blank=True, default=0)),
                ('unit_price', models.IntegerField(blank=True, default=0)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_loc_list', to='board.location')),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_list', to='board.product')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_unit_list', to='board.unit')),
            ],
        ),
    ]

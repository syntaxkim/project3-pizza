# Generated by Django 2.1.3 on 2018-11-29 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0009_auto_20181128_2231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.IntegerField(default=0, verbose_name='Shipment Total')),
                ('order_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Order placed')),
                ('billing_address', models.CharField(max_length=100)),
                ('shipping_address', models.CharField(max_length=100)),
                ('message', models.CharField(blank=True, max_length=50)),
                ('status', models.CharField(choices=[('Ordered', 'Ordered'), ('On Shipping', 'On Shipping'), ('Delivered', 'Delivered')], default='Ordered', max_length=16)),
                ('recieved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('extra', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Item')),
                ('toppings', models.ManyToManyField(blank=True, related_name='orders', to='orders.Topping')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='toppings',
            field=models.ManyToManyField(blank=True, related_name='carts', to='orders.Topping'),
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='order', to='orders.OrderItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL),
        ),
    ]

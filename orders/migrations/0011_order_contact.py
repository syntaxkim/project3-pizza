# Generated by Django 2.1.3 on 2018-11-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20181129_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact',
            field=models.CharField(default='010', max_length=100),
            preserve_default=False,
        ),
    ]

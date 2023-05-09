# Generated by Django 4.1.7 on 2023-05-03 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='username',
            new_name='buyer_username',
        ),
        migrations.AddField(
            model_name='orders',
            name='seller_username',
            field=models.CharField(default='alice', max_length=100),
            preserve_default=False,
        ),
    ]

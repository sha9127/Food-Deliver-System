# Generated by Django 3.1.5 on 2022-03-11 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0005_auto_20220311_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='media/'),
        ),
    ]

# Generated by Django 3.1.5 on 2022-03-11 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0007_auto_20220311_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='Food_Detail'),
        ),
    ]

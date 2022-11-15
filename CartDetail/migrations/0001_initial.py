# Generated by Django 3.1.5 on 2022-03-03 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('browse', '0003_auto_20220303_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(max_length=50)),
                ('is_ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='browse.fooditem')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='browse.restaurant_detail')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

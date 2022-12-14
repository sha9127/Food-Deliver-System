# Generated by Django 3.1.5 on 2022-03-03 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant_Detail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('ratings', models.DecimalField(decimal_places=2, max_digits=5)),
                ('category', models.ManyToManyField(to='users.Category')),
                ('restaurant_user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('food_item', models.JSONField(default=dict)),
                ('total_price', models.DecimalField(blank=True,
                 decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Order Received', 'Order Received'), ('Cooking', 'Cooking'), (
                    'Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=150)),
                ('restaurant', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='browse.restaurant_detail')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(
                    default='default.jpg', upload_to='Food_Detail/')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('food_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('category', models.ManyToManyField(to='users.Category')),
                ('restaurant', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='browse.restaurant_detail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                 editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(max_length=50)),
                ('is_ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1, null=True)),
                ('price', models.DecimalField(blank=True,
                 decimal_places=2, max_digits=5, null=True)),
                ('customer', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.CASCADE, to='browse.fooditem')),
                ('restaurant', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.CASCADE, to='browse.restaurant_detail')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

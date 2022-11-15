from django.db import models
from users.models import BaseModel, User
from browse.models import Restaurant_Detail

# Create your models here.


class Order(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant_Detail, on_delete=models.CASCADE)
    food_item = models.JSONField(default=dict)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    orderstatuses = (
        ('Pending', 'Pending'),
        ('Order Received', 'Order Received'),
        ('Cooking', 'Cooking'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Order Cancelled', 'Order Cancelled'),
    )
    order_status_history = {
        'Pending': None,
        'Order Received': None,
        'Cooking': None,
        'Out_for_Delivery': None,
        'Delivered': None, }

    status = models.CharField(
        max_length=150, choices=orderstatuses, default='Pending')
    status1 = models.JSONField(default=dict)

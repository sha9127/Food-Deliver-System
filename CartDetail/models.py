from django.db import models
from users.models import BaseModel, User
from browse.models import Restaurant_Detail, FoodItem


class Cart(BaseModel):

    restaurant = models.ForeignKey(
        Restaurant_Detail, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=50)
    item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(null=True, default=1)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

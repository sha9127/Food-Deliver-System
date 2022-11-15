from django.contrib import admin
from .models import NotificationsRestaurant, NotificationsUser, Restaurant_Detail, FoodItem, Category, Token
# Register your models here.
admin.site.register(Restaurant_Detail)
admin.site.register(FoodItem)
admin.site.register(Category)
admin.site.register(Token)
admin.site.register(NotificationsUser)
admin.site.register(NotificationsRestaurant)

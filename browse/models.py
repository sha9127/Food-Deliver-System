from django.db import models
from users.models import BaseModel, User
# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class Restaurant_Detail(BaseModel):
    restaurant_user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    ratings = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    @staticmethod
    def get_all_profile():
        return Restaurant_Detail.objects.all()

    @staticmethod
    def get_profile_by_search(data):
        if data:
            return Restaurant_Detail.objects.filter(restaurant_user=data)
        else:
            return Restaurant_Detail.objects.all()

    @staticmethod
    def create_instance(data):
        return Restaurant_Detail.objects.create(**data)

    @staticmethod
    def update_instance(data):
        return Restaurant_Detail.objects.update(**data)


class FoodItem(BaseModel):
    image = models.ImageField(default='default.jpg',
                              upload_to='Food_Detail')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField(Category)
    restaurant = models.ForeignKey(
        Restaurant_Detail, on_delete=models.CASCADE)
    food_id = models.IntegerField(unique=True, blank=True, null=True)

    @staticmethod
    def get_all_food():
        return FoodItem.objects.all()

    @staticmethod
    def get_food_by_categoryid(category_id):
        if category_id:
            return FoodItem.objects.filter(category=category_id)
        else:
            return FoodItem.objects.all()

    @staticmethod
    def create_instance(data):
        return FoodItem.objects.create(**data)

    @staticmethod
    def update_instance(data):
        return FoodItem.objects.update(**data)


class NotificationsRestaurant(BaseModel):

    sender = models.ForeignKey(
        User, related_name="sender", on_delete=models.CASCADE)

    receiver = models.ForeignKey(
        Restaurant_Detail, related_name="receiver", on_delete=models.CASCADE)

    title = models.CharField(max_length=255)

    text = models.TextField(max_length=1000)

    is_seen = models.BooleanField(default=False)


class NotificationsUser(BaseModel):

    sender = models.ForeignKey(
        Restaurant_Detail, related_name="sender", on_delete=models.CASCADE)

    receiver = models.ForeignKey(
        User, related_name="receiver", on_delete=models.CASCADE)

    title = models.CharField(max_length=255)

    text = models.TextField(max_length=1000)

    is_seen = models.BooleanField(default=False)


class Token(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    token = models.CharField(max_length=255)

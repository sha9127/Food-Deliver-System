from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Restaurant_Detail, FoodItem, Category, Token
from users.models import User
from CartDetail.models import Cart
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import requests

# Create your views here.

# 1 -- Home Page


class Home(View):

    def get(self, request):

        return render(request, 'home.html')

# 2--Search


class Search(View):

    def get(self, request):

        restaurant = Restaurant_Detail.objects.select_related(
            'restaurant_user').all().exclude(restaurant_user=request.user.id)
        user = User.objects.all().order_by('-name').exclude(id=request.user.id)
        search = request.GET.get('search')

        if search != None:
            user = User.objects.get(name=search)
            restaurant = Restaurant_Detail.get_profile_by_search(user.id).select_related(
                'restaurant_user')

        data = {'restaurant': restaurant,  'title': 'Search'}

        return render(request, 'search.html', data)


# 3-- Creating  Restaurant Profile


class RestaurantProfile(View):

    def get(self, request):

        category = Category.objects.all()
        rest = User.objects.get(id=request.user.id)
        restaurant = Restaurant_Detail.objects.filter(restaurant_user=rest)
        context = {'categories': category, 'restaurant': restaurant}
        return render(request, 'rprofile.html', context)

    def post(self, request):

        option = request.POST.getlist('category')
        rest = User.objects.get(id=request.user.id)
        data = dict(request.POST.items())
        data.pop('csrfmiddlewaretoken')
        data['restaurant_user'] = rest

        if 'submit' in request.POST:

            data.pop('submit')
            data.pop('category')
            instance = Restaurant_Detail.objects.create(**data)
            category = Category.objects.filter(name__in=option)
            for i in category:
                instance.category.add(i)
            return redirect('rprofile')

        if 'update' in request.POST:

            data.pop('update')
            current_restaurant = User.objects.get(id=request.user.id)
            instance = Restaurant_Detail.objects.filter(
                restaurant_user=current_restaurant).update(**data)
            category = Category.objects.filter(name__in=option)
            for i in category:
                instance.category.add(i)
            messages.success(request, 'Deatail Update Sucessfully !')
            return redirect('rprofile')

        if 'remove' in request.POST:

            instance = Restaurant_Detail.objects.get(
                restaurant_user=request.user)
            for i in category:
                instance.category.remove(i)
            return redirect('rprofile')

        return redirect('rprofile')


# 4 -- Restaurant Menu


class Menu(View):

    def get(self, request):

        categories = Category.objects.all()
        myuser = User.objects.get(
            id=request.user.id)
        data = ''
        foods = ''

        if myuser.role.name == 'Restaurant':
            data = Restaurant_Detail.objects.get(
                restaurant_user=request.user.id)
            foods = FoodItem.objects.filter(restaurant=data)
            item = Restaurant_Detail.objects.filter(
                restaurant_user=request.user.id)

        context = {'data': data, 'foods': foods,
                   'categories': categories, 'title': 'Profile-Restaurant', 'item': item}

        return render(request, 'restaurant_profile.html', context)

    def post(self, request):

        image = request.FILES.get('image')
        print(image)
        data = request.POST.items()
        food_item = dict(data)
        food_item.pop('csrfmiddlewaretoken')
        food_item.pop('update')
        user = User.objects.get(id=request.user.id)
        restaurant = Restaurant_Detail.objects.get(restaurant_user=user)
        food_item['restaurant'] = restaurant
        food_item['image'] = image

        if 'update' in request.POST:
            FoodItem.objects.filter(id=food_item['id']).update(**food_item)
            messages.success(request, 'You Item Updated Sucessfully ')
            return render(request, 'restaurant_profile.html')

        elif 'delete' in request.POST:
            m = FoodItem.objects.get(id=id)
            m.delete()
            messages.success(request, 'You Item Deleted Sucessfully ')
            return redirect('restaurant-profile')

        else:
            return render(request, 'restaurant_profile.html')


def get_absolute_url(self):

    return reverse('profile-rest', kwargs={'id': self.id})


# 5-- Add item to Restaurant Menu


class AddItem(View):

    def post(self, request):

        image = request.FILES.get('image')
        data = request.POST.items()
        item = dict(data)
        item.pop('csrfmiddlewaretoken')
        item.pop('add')
        user = User.objects.get(id=request.user.id)
        restaurant = Restaurant_Detail.objects.get(restaurant_user=user)
        item['restaurant'] = restaurant
        item['image'] = image
        FoodItem.objects.create(**item)
        messages.success(request, 'You Item Added Sucessfully ')
        return render(request, 'additem.html')

    def get(self, request):

        return render(request, 'additem.html')

# 6-- Add Item  to Cart


class AddToCart(View):

    def post(self, request, restaurant_id):

        item_id = request.POST.get('food_id')
        price = request.POST.get('price')
        quantity = request.POST.get('option')
        restaurant = Restaurant_Detail.objects.get(id=restaurant_id)
        fooditem = FoodItem.objects.get(restaurant=restaurant, id=item_id)
        cart = Cart.objects.filter(customer=request.user.id, is_ordered=False)

        check_restaurant = cart.filter(restaurant__id=restaurant_id)
        add_to_cart = False

        if len(cart) == 0:
            add_to_cart = True
        elif len(cart) > 0 and len(check_restaurant) > 0:
            add_to_cart = True

        if add_to_cart:
            obj, created = Cart.objects.update_or_create(customer=request.user, item=fooditem,
                                                         restaurant=restaurant, defaults={'quantity': quantity, 'address': request.user.address, 'price': price, 'is_ordered': False})
            messages.success(
                request, 'You Item Added to your Cart ')
        else:
            messages.warning(
                request, 'Empty your Cart to add Item')

        return redirect('cart-detail')

    def get(self, request, restaurant_id):

        qty = range(1, 11)
        ins = Restaurant_Detail.objects.get(id=restaurant_id)
        item = FoodItem.objects.filter(restaurant=ins)
        context = {'foods': item, 'qty': qty, 'title': 'Order'}
        return render(request, 'profile_rest.html', context)


# -- Sending Token to Backend

def send_token(request):

    if request.is_ajax and request.method == "POST":

        token = request.POST.get('registration_id')

        data = {}
        print(token)

        fcmToken, created = Token.objects.get_or_create(
            user=request.user, token=token)

        if not created:

            data = {"userToken": "already added"}

        else:

            data = {"userToken": "added"}

    return JsonResponse(data)


# Sending Notification

def send_notification(registration_ids, message_title, message_desc):

    fcm_api = "AAAAakMsPXw:APA91bEu8PmO_I_LOvjq6jZqzwmVRY87_ZFoPSdlV0fUEylyd7lB2BuWXOTn5gCxV_sDqLLGrg2cUP2tQfkNiB1vQKQj8H6MwwlRB6NEzQtaFBFlKe-tf0RpW-N5xcOSUY5GlWDkmtFs"

    url = "https://fcm.googleapis.com/fcm/send"

    headers = {

        "Content-Type": "application/json",

        "Authorization": 'key='+fcm_api}

    payload = {

        "registration_ids": registration_ids,

        "priority": "high",

        "notification": {

            "body": message_desc,

            "title": message_title,

            "image": "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
        }

    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers)

    print(result.json())

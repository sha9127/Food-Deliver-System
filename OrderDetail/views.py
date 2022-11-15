from datetime import datetime
from django.dispatch import receiver
from django.shortcuts import render, redirect
from browse.views import send_notification
from .models import Order
from django.views import View
from CartDetail.models import Cart
import json
from decimal import Decimal
from django.contrib import messages
from users.models import User
from browse.models import NotificationsRestaurant, Restaurant_Detail, Token, NotificationsUser

# Create your views here.

# 1-- Order History of Customer


class Orders(View):

    def get(self, request):

        query = Order.objects.filter(
            user=request.user.id).order_by('-created_date')
        context = {'name': request.user.name,
                   'address': request.user.address, 'query': query}
        return render(request, 'order.html', context)

# 2-- Order Placing and saving Item to Json Field


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return "%.2f" % obj
        return json.JSONEncoder.default(self, obj)


class Success(View):

    def get(self, request):

        cart_items = Cart.objects.filter(
            customer=request.user, is_ordered=False)

        print(cart_items)
        order_items = []
        total_price = 0
        i = 0
        for item in cart_items:

            order_items.append({'name': item.item.title,
                                'quantity': item.quantity, 'price': item.price})
            total_price += item.quantity * item.price

        with open("fooditem.json", "w") as outfile:
            json.dump(order_items, outfile, cls=DecimalEncoder)

        f = open('fooditem.json')
        data = json.load(f)
        for i in data:
            print(i)

        for item in cart_items:
            restaurant = item.restaurant
            break

        check_cart = False
        if len(cart_items) > 0:
            check_cart = True

        if check_cart:
            Order.objects.create(
                user=request.user, restaurant=restaurant, food_item=data, total_price=total_price)
            NotificationsRestaurant.objects.create(
                sender=request.user, receiver=restaurant, title='Order Status', text='Test')
            registration_id = Token.objects.filter(
                user=restaurant.restaurant_user).first()
            print(registration_id.token)
            notification = NotificationsRestaurant(sender=request.user)
            send_notification([registration_id.token],
                              notification.title, notification.text)
            cart_items.update(is_ordered=True)

            a = {}
            a['Pending'] = datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%SZ")

            with open("default.json", "r") as outfile:
                data = json.load(outfile)
            print(data)

            data.update(a)

            with open("default.json", "w") as outfile:
                json.dump(data, outfile)

            messages.success(request, 'Order Placed Sucessfully !!')

        return redirect('order')


# 9-- Order Dashboard for Restaurant


class Dashboard(View):

    def get(self, request):

        user = User.objects.get(id=request.user.id)
        restaurant_id = Restaurant_Detail.objects.get(restaurant_user=user)
        query = Order.objects.filter(
            restaurant=restaurant_id).order_by('-created_date')
        order_status = Order.orderstatuses
        context = {'name': request.user.name,
                   'address': request.user.address, 'query': query,  'order': order_status}
        return render(request, 'dashboard.html', context)

    def post(self, request):

        id = request.POST.get('id')
        # option = request.POST.get('option')
        options = request.POST.get('options')
        item = Order.objects.get(id=id)
        print(len(item.status1))

        a = {}
        a[options] = datetime.now().strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        if len(item.status1):
            with open("order_history.json", "r") as outfile:
                data = json.load(outfile)

            data.update(a)

            with open("order_history.json", "w") as outfile:
                json.dump(data, outfile)
        else:
            with open("default.json", "r") as outfile:
                data = json.load(outfile)

            data.update(a)

            with open("order_history.json", "w") as outfile:
                json.dump(data, outfile)

        f = open('order_history.json')
        data = json.load(f)
        for i in data:
            print(i)

        if 'status' in request.POST:
            # item.status = option
            item.status1 = data
            item.save()
            NotificationsUser.objects.create(
                sender=item.restaurant, receiver=item.user, title='Order Status', text='Test')
            registration_id = Token.objects.filter(
                user=item.user).first()
            print(registration_id.token)
            notification = NotificationsUser(
                sender=item.restaurant)
            send_notification([registration_id.token],
                              notification.title, notification.text)
            messages.success(request, ' Order Status Updated !!! ')

            return redirect('dashboard')

        else:
            return render(request, 'dashboard.html')

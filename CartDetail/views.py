from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Cart
from users.models import User

# Create your views here.

# 1-- Added items in Customer's Cart


class CartDetail(View):

    def get(self, request):

        current_customer = User.objects.get(id=request.user.id)
        cart = Cart.objects.filter(
            customer=current_customer, is_ordered=False)
        total_price = 0
        for i in cart:
            total_price += i.price*i.quantity
        print(total_price)
        context = {'c': cart, 'name': request.user.name,
                   'address': request.user.address, 'total_price': total_price}

        return render(request, 'cart_detail.html', context)

    def post(self, request):

        id = request.POST.get('id')
        print(id)
        m = Cart.objects.get(id=id)
        if 'delete' in request.POST:
            m.delete()
            messages.success(request, 'You Item Deleted Sucessfully ')
            return redirect('cart-detail')

        else:
            return redirect('order')

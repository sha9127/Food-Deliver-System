from . import views
from django.urls import path

urlpatterns = [

    path('cart_detail',
         views.CartDetail.as_view(), name='cart-detail'),
]

from . import views
from django.urls import path

urlpatterns = [


    path('order/',
         views.Orders.as_view(), name='order'),
    path('order/sucess/',
         views.Success.as_view(), name='success'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]

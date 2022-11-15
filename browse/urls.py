from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('search/', views.Search.as_view(), name='search'),
    path('restaurant-profile/', views.Menu.as_view(),
         name='restaurant-profile'),
    path('search/profile-rest/<uuid:restaurant_id>/', views.AddToCart.as_view(),
         name='profile-rest'),
    path('restaurant-profile/additem/', views.AddItem.as_view(), name='addItem'),
    path('rprofile/', views.RestaurantProfile.as_view(), name='rprofile'),
    path("firebase-messaging-sw.js",
         TemplateView.as_view(
             template_name="firebase-messaging-sw.js",
             content_type="application/javascript",
         ),
         name="firebase-messaging-sw.js"
         ),
    path('test/', views.send_token, name='test'),


]

from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='login'),
    path('signout/', views.SignOut.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.Profile.as_view(), name='profile'),

]

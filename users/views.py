from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, Role
from browse.models import Restaurant_Detail
from django.urls import reverse
from django.views import View


# Create your views here.

# 1 -- Sign-Up


class SignUp(View):

    def get(self, request):

        roles = Role.objects.all()
        context = {'roles': roles, 'title': 'Sign-Up'}
        return render(request, 'signup.html', context)

    def post(self, request):

        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if role == 'Customer':
            role = Role.objects.get(name='Customer')
        else:
            role = Role.objects.get(name='Restaurant')
        myuser = User.objects.create_user(
            email=email, password=password1, name=name, address=address, role=role)
        myuser.save()
        messages.success(
            request, 'Your acoount has been created Sucessfully !!!')
        return render(request, 'signup.html')


# 2-- Sign-In

class SignIn(View):

    def get(self, request):

        context = {'title': 'Sign-In'}
        return render(request, 'login.html', context)

    def post(self, request):

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            restaurant = Restaurant_Detail.objects.all()
            context = {'a': restaurant}
            return render(request, 'search.html', context)
        else:
            messages.error(request, 'Bad credentials !!!')
            return redirect('login')

# 3-- Sign-Out


class SignOut(View):

    def get(self, request):

        logout(request)
        messages.success(request, 'You are sucessfully logout !!!')
        return redirect('home')


# 4-- User Profile


class Profile(View):

    def get(self, request):

        context = {'profile': request.user, 'title': 'Profile'}
        return render(request, 'profile.html', context)

    def post(self, request):

        data = request.POST.items()
        user_data = dict(data)
        user_data.pop('csrfmiddlewaretoken')
        User.objects.filter(
            id=request.user.id).update(**user_data)
        messages.success(
            request, 'Your acoount has been Updated Sucessfully !!!')
        return render(request, 'profile.html')

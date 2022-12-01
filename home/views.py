from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegisterForm
from django.urls import reverse_lazy
from user_profile.models import OwnerProfilePhoto
from add.tests import pint
from add.models import (Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo, Favrioute)
from django.db.models import Count



# Create your views here.

class RegisterView(View):

    sucess_url = reverse_lazy('home:all')
    
    def get(self, request):
        fm = RegisterForm()
        contx = {'form':fm}
        return render(request, 'home/register.html', contx)

    def post(self, request):
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            user =fm.save()
            pro_pic = OwnerProfilePhoto(owner=user)
            pro_pic.save()
            return redirect(self.sucess_url)
        contx = {'form':fm}
        return render(request, 'home/register.html', contx)
        

class HomeView(View):

    def get(self, request):
        if request.user.is_authenticated:
            count_list = Category.recemondation.user_recemondations()
        else:
            count_list = Category.recemondation.anonomous_user_recemondations()
        contx = {'count_list':count_list}
        return render(request, 'home/home.html', contx)
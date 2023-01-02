"""
HOME VIEW MODULE
----------------
This module used to store all the views related to home app 
"""



from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegisterForm
from django.urls import reverse_lazy
from user_profile.models import OwnerProfilePhoto
from add.tests import pint
from add.models import (Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo, Favrioute)
from django.db.models import Count
import asyncio
from django.core.handlers.asgi import ASGIRequest


# Create your views here.

class RegisterView(View):
    """A view for registering new users."""

    sucess_url = reverse_lazy('home:all')
    
    def get(self, request):
        """
        Displays RigisterForm

        :param request: ASGIRequest
        :context: 
            form: An instance of form class RegisterForm
        :return: HttpResponse
        """

        fm = RegisterForm()
        contx = {'form':fm}
        return render(request, 'home/register.html', contx)

    def post(self, request):
        """
        Creates a new user
        :param request: ASGIRequest
        :context: 
            form: An instance of form class RegisterForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        fm = RegisterForm(request.POST)
        if fm.is_valid():
            user =fm.save()
            pro_pic = OwnerProfilePhoto(owner=user) # creating a blank user profile photo
            pro_pic.save() # saving a blank user profile photo
            return redirect(self.sucess_url)
        contx = {'form':fm}
        return render(request, 'home/register.html', contx)
        

class HomeView(View):
    """A view for displaying homepage."""

    def get(self, request):
        """
        Displays homepage with recommendation

        :param request: ASGIRequest
        :context: 
            count_list: An instance of model class Category
        :return: HttpResponse
        """

        if request.user.is_authenticated:
            count_list = Category.recemondation.user_recemondations() #custom manager method
        else:
            count_list = Category.recemondation.anonomous_user_recemondations() #custom manager method
        contx = {'count_list':count_list}
        return render(request, 'home/home.html', contx)
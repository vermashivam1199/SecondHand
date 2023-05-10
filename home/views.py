"""
HOME VIEW MODULE
----------------
This module used to store all the views related to home app 
"""



from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegisterForm
from .models import UserUuid
from django.urls import reverse_lazy
from user_profile.models import OwnerProfilePhoto
from add.tests import pint
from add.models import (Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo, Favrioute)
from django.db.models import Count
import asyncio
from django.core.handlers.asgi import ASGIRequest
from secondhand.tasks import test_funk
from django.core.paginator import Paginator
from add.views import PaginationView
from asgiref.sync import sync_to_async



# Create your views here.

class RegisterView(View):
    """A view for registering new users."""

    sucess_url = reverse_lazy('home:all')
    
    def get(self, request):
        """
        Displays RigisterForm

        :param ASGIRequest request: Request object
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
        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class RegisterForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        fm = RegisterForm(request.POST)
        if fm.is_valid():
            user =fm.save()
            user_uuid = UserUuid(user=user)
            user_uuid.save() #creating seprate uuid for each user
            pro_pic = OwnerProfilePhoto(owner=user) # creating a blank user profile photo
            pro_pic.save() # saving a blank user profile photo
            return redirect(self.sucess_url)
        contx = {'form':fm}
        return render(request, 'home/register.html', contx)
        

class HomeView(View, PaginationView):
    """A view for displaying homepage."""

    async def get(self, request):
        """
        Displays homepage with recommendation

        :param ASGIRequest request: Request object
        :context: 
            count_list: An instance of model class Category
        :return: HttpResponse
        """

        if request.user.is_authenticated:
            count_list = await sync_to_async(Category.recemondation.user_recemondations)(self.request.user.id) #custom manager method
        else:
            count_list = await sync_to_async(Category.recemondation.anonomous_user_recemondations)() #custom manager method
        count_list = list(count_list)
        paginator = Paginator(count_list, 2)
        page_number = request.GET.get("page")
        pint(page_number, "home page")
        page_obj = paginator.get_page(page_number)
        total_pages = await self.helper_max_page(page_obj.number, paginator.num_pages)
        next_page, previous_page = await self.helper_next_previous_page(page_obj)
        contx = {
            "final_list": page_obj, "total_pages": total_pages, 
            "current_page": page_obj.number, "next_page": next_page, "previous_page": previous_page
        }
        return render(request, 'home/home.html', contx)
    
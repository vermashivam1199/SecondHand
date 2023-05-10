"""
HOME VIEW MODULE
----------------
This module used to store all the views related to user_profile app 
"""


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import OwnerProfilePhoto
from .forms import OwnerProfilePhotoForm, UserUpdateForm
from django.http import HttpResponse
from add.tests import pint
from add.models import Category, Favrioute
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import asyncio
from asgiref.sync import sync_to_async
from add.models import Comment, Saved, OfferedPrice, AddHistory, Add
from django.db.models import Q, Count
import json
from django.core.paginator import Paginator
from add.views import PaginationView

# Create your views here.

class UserProfileView(LoginRequiredMixin, View, PaginationView):
    """A view to display user profile"""

    sucess_url = reverse_lazy('add:add_list')

    async def get(self, request):
        """
        Displays user profile page

        :param ASGIRequest request: Request object
        :context: 
            owner: An instance of model class User
            categories: A list containing instance of model class Category
            favrioute: A list of category IDs that used has set to favrioute
        :return: HttpResponse
        """

        u = request.user
        categories, fav, total_comments_dict, total_views_dict, total_offer_price_dict, total_saved_dict, adds = await asyncio.gather(
            self.helper_cat(), self.helper_fav(), self.helper_total_comments(), self.helper_total_views(), 
            self.helper_total_offer_price(), self.helper_total_saved(), self.helper_add()
        )
        favr = [f['id'] for f in fav] # creating a list of category IDs that user has set to favrioute 
        paginator = Paginator(adds, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        total_pages = await self.helper_max_page(page_obj.number, paginator.num_pages)
        next_page, previous_page = await self.helper_next_previous_page(page_obj)
        contx = {
            'owner':u, 'categories':categories, 'favrioute':favr, "total_views_dict":total_views_dict, "total_saved_dict":total_saved_dict,
            "total_comments_dict":total_comments_dict, "total_offer_price_dict":total_offer_price_dict, "final_list": page_obj, "total_pages": total_pages, 
            "current_page": page_obj.number, "next_page": next_page, "previous_page": previous_page
        }
        return await sync_to_async(render)(request, 'user_profile/owner_home.html', contx)
        
    @sync_to_async
    def helper_total_comments(self):
        com = list(Comment.graph.total_value(self.request.user))
        pint(com)
        x_axis = [str(i["created_at__date"]) for i in com]
        y_axis = [i["total"] for i in com]
        pint(x_axis)
        pint(y_axis)
        total_comments_dict = {k:v for k,v in zip(x_axis, y_axis)}
        total_comments_dict = json.dumps(total_comments_dict)
        return total_comments_dict

    @sync_to_async
    def helper_total_views(self):
        com = AddHistory.graph.total_value(self.request.user)
        x_axis = [str(i["created_at__date"]) for i in com]
        y_axis = [i["total"] for i in com]
        pint(x_axis)
        pint(y_axis)
        total_views_dict = {k:v for k,v in zip(x_axis, y_axis)}
        total_views_dict = json.dumps(total_views_dict)
        return total_views_dict
    
    @sync_to_async
    def helper_total_offer_price(self):
        com = OfferedPrice.graph.total_value(self.request.user)
        x_axis = [str(i["created_at__date"]) for i in com]
        y_axis = [i["total"] for i in com]
        pint(x_axis)
        pint(y_axis)
        total_offer_price_dict = {k:v for k,v in zip(x_axis, y_axis)}
        total_offer_price_dict = json.dumps(total_offer_price_dict)
        return total_offer_price_dict
    
    @sync_to_async
    def helper_total_saved(self):
        com = Saved.graph.total_value(self.request.user)
        x_axis = [str(i["created_at__date"]) for i in com]
        y_axis = [i["total"] for i in com]
        pint(x_axis)
        pint(y_axis)
        total_saved_dict = {k:v for k,v in zip(x_axis, y_axis)}
        total_saved_dict = json.dumps(total_saved_dict)
        return total_saved_dict
    
    @sync_to_async(thread_sensitive=False)
    def helper_add(self):
        """A helper method that returns User object through sync_to_async decorator"""

        o = Add.objects.filter(owner=self.request.user)
        return list(o)
    
    @sync_to_async(thread_sensitive=False)
    def helper_cat(self):
        """A helper method that returns list of Category objects through sync_to_async decorator"""

        l = Category.objects.all()
        return list(l)
    
    @sync_to_async(thread_sensitive=False)
    def helper_fav(self):
        """A helper method that returns list of Category object which are favrioutes of current logged in user through sync_to_async decorator"""

        l = self.request.user.user_category_favrioute.values('id')
        return list(l)



class OwnerProfilePhotoUpdateView(LoginRequiredMixin, View):
    """A view to update profile photo of users."""


    def get(self, request):
        """
        Displays user's profile photo update form

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class OwnerProfilePhotoForm
        :return: HttpResponse
        """

        fm = OwnerProfilePhotoForm()
        ctx = {'form':fm}
        return render(request, 'user_profile/profile_photo.html', ctx)

    def post(self, request):
        """
        Updates a user's profile photo

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class OwnerProfilePhotoForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        owner = request.user
        pic = get_object_or_404(OwnerProfilePhoto, owner=owner)
        fm = OwnerProfilePhotoForm(request.POST, request.FILES or None, instance=pic)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('user_profile:profile_page'))
        ctx = {'form':fm}
        return render(request, 'user_profile/profile_photo.html', ctx)


def stream_profile_pic(request):
    """
    this view function displays returns user's profile photo

    :param ASGIRequest request: Request object
    :return: HttpResponse
    """

    pic = get_object_or_404(OwnerProfilePhoto, owner=request.user)
    response = HttpResponse()
    if pic.content_type:
        response['Content-Type'] = pic.content_type
        response['Content-Length'] = len(pic.picture)
        response.write(pic.picture)
    return response



class OwnerProfilePhotoDeleteView(LoginRequiredMixin, View):
    """This view deletes user's profile photo"""

    def get(self, request):
        """
        Displays profile picture delete form

        :param ASGIRequest request: Request object
        :return: HttpResponse
        """

        ctx = {}
        return render(request, 'add/delete.html', ctx)

    def post(self, request):
        """
        Deletes user's profile picture

        :param ASGIRequest request: Request object
        :return: HttpResponseRedirect
        """

        owner = request.user
        pic = get_object_or_404(OwnerProfilePhoto, owner=owner)
        pic.picture = None
        pic.content_type = None
        pic.save()
        return redirect(reverse('user_profile:profile_page'))


class OwnerAboutView(View):
    """Displays add owner profile page"""

    def get(self, request, pk):
        """
        Displays add owner profile page

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class OwnerProfilePhotoForm
        :return: HttpResponse
        """

        owner = get_object_or_404(User, pk=pk)
        contx = {'owner':owner}
        return render(request, 'user_profile/owner_about.html', contx)




@method_decorator(csrf_exempt, name='dispatch')
class CreateFavriouteView(LoginRequiredMixin, View):
    """ This view creates an instance of Favrioute modle class"""

    def post(self, request, pk):
        """
        Creates an instance of Favrioute modle class

        :param ASGIRequest request: Request object
        :param int pk: primary key of Catagory model
        :return: HttpResponse
        """

        c = get_object_or_404(Category, pk=pk)
        sav = Favrioute(owner=request.user, category=c)
        try:
            sav.save()
        except IntegrityError: # If there is already a row with same user and Add
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavriouteView(LoginRequiredMixin, View):
    """This view deletes instance of Favrioute modle class"""

    def post(self, request, pk):
        """
        Deletes an instance of Favrioute modle class

        :param ASGIRequest request: Request object
        :param int pk: primary key of Catagory model
        :return: HttpResponse
        """

        c = get_object_or_404(Category, pk=pk)
        try:
            Favrioute.objects.get(owner=request.user, category= c).delete()
        except Favrioute.DoesNotExist as e:
            pass
        return HttpResponse()

class UserUpdateView(LoginRequiredMixin, View):
    """This view updates user's information"""

    def get(self, request):
        """
        Displays UserUpdateForm

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class UserUpdateForm
        :return: HttpResponse
        """
        fm = UserUpdateForm(instance=request.user)
        contx = {'form':fm}
        return render(request, 'user_profile/user_update.html', contx)

    def post(self, request):
        """
        Updates instance of User model class

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class UserUpdateForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        fm = UserUpdateForm(request.POST, instance=request.user)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('user_profile:profile_page'))
        contx = {'form':fm}
        return render(request, 'user_profie/user_update.html', contx)



class PasswordUpdateView(LoginRequiredMixin, View):
    """This view updates user's password"""

    def get(self, request):
        """
        Displays PasswordChangeForm

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class UserUpdateForm
        :return: HttpResponse
        """

        fm = PasswordChangeForm(user=request.user)
        contx = {'form':fm}
        return render(request, 'user_profile/user_update.html', contx)

    def post(self, request):
        """
        Updates user password

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class UserUpdateForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        fm = PasswordChangeForm(user=request.user, data=request.POST or None)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            return redirect(reverse('user_profile:profile_page'))
        contx = {'form':fm}
        return render(request, 'user_profile/user_update.html', contx)


def stream_profile_pic_chat(request, pk):
    """
    this view function displays returns user's profile photo

    :param ASGIRequest request: Request object
    :return: HttpResponse
    """

    owner = get_object_or_404(User, pk=pk)
    pic = get_object_or_404(OwnerProfilePhoto, owner=owner)
    response = HttpResponse()
    if pic.content_type:
        pint('stream view working')
        response['Content-Type'] = pic.content_type
        response['Content-Length'] = len(pic.picture)
        response.write(pic.picture)
    return response


class DashboardDetailView(LoginRequiredMixin, View):

    async def get(self, request, pk):
        add = await sync_to_async(get_object_or_404)(Add, pk=pk)
        total_comments_dict, total_views_dict, total_offer_price_dict, total_saved_dict = await asyncio.gather(
            self.helper_detail_comment(add), self.helper_detail_views(add), 
            self.helper_detail_offered_price(add), self.helper_detail_saved(add)
        )
        pint(total_comments_dict, "comments dict")
        contx = {
            "total_views_dict":total_views_dict, "total_saved_dict":total_saved_dict,
            "total_comments_dict":total_comments_dict, "total_offer_price_dict":total_offer_price_dict,
            "add_id":add.id
        }

        return render(request, "user_profile/dashboard_deatil.html", contx)
    
    @sync_to_async
    def helper_detail_views(self, a):
        r = AddHistory.detail_graph.total_value_detail(a)
        x_axis = [str(i["created_at__date"]) for i in r]
        y_axis = [i["total"] for i in r]
        pint("views")
        pint(x_axis)
        pint(y_axis)
        total_views_dict = {k:v for k,v in zip(x_axis, y_axis)}
        total_views_dict = json.dumps(total_views_dict)
        return total_views_dict
    
    @sync_to_async
    def helper_detail_comment(self, a):
        r = Comment.detail_graph.total_value_detail(a)
        x_axis = [str(i["created_at__date"]) for i in r]
        y_axis = [i["total"] for i in r]
        pint("comments")
        pint(x_axis)
        pint(y_axis)
        total_comments_dict = {k:v for k,v in zip(x_axis, y_axis)}
        total_comments_dict = json.dumps(total_comments_dict)
        pint(total_comments_dict)
        return total_comments_dict
    
    @sync_to_async
    def helper_detail_saved(self, a):
        r = Saved.detail_graph.total_value_detail(a)
        x_axis = [str(i["created_at__date"]) for i in r]
        y_axis = [i["total"] for i in r]
        pint("saved")
        pint(x_axis)
        pint(y_axis)
        total_saved_dict = {k:v for k,v in zip(x_axis, y_axis)}
        total_saved_dict = json.dumps(total_saved_dict)
        pint(type(total_saved_dict))
        return total_saved_dict
    
    @sync_to_async
    def helper_detail_offered_price(self, a):
        r = OfferedPrice.detail_graph.total_value_detail(a)
        x_axis = [str(i["created_at__date"]) for i in r]
        y_axis = [i["total"] for i in r]
        pint("offer price")
        pint(x_axis)
        pint(y_axis)
        total_offered_price_dict = {k:v for k,v in zip(x_axis, y_axis)}
        total_offered_price_dict = json.dumps(total_offered_price_dict)
        return total_offered_price_dict
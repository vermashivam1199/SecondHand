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
from .models import OwnerProfilePhoto, Chat, UserMessage
from .forms import OwnerProfilePhotoForm, ChatForm, UserUpdateForm
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

# Create your views here.

class UserProfileView(LoginRequiredMixin, View):
    """A view to display user profile"""

    sucess_url = reverse_lazy('add:add_list')

    async def get(self, request):
        """
        Displays user profile page

        :param request: ASGIRequest
        :context: 
            owner: An instance of model class User
            categories: A list containing instance of model class Category
            favrioute: A list of category IDs that used has set to favrioute
        :return: HttpResponse
        """

        if 'pk' in request.session:
            del request.session['pk']

        u, categories = await asyncio.gather(self.helper_user(), self.helper_cat())
        pint(categories)
        if request.user.is_authenticated:
            fav = await self.helper_fav() # returns list of catagories in form of dict objects that user has set to favrioute
            favr = [f['id'] for f in fav] # creating a list of category IDs that user has set to favrioute 
        contx = {'owner':u, 'categories':categories, 'favrioute':favr}
        return render(request, 'user_profile/owner_home.html', contx)

    @sync_to_async(thread_sensitive=False)
    def helper_user(self):
        """A helper method that returns User object through sync_to_async decorator"""

        o = get_object_or_404(User, pk=self.request.user.id)
        return o
    
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

        :param request: ASGIRequest
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

        :param request: ASGIRequest
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

    :param request: ASGIRequest
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

        :param request: ASGIRequest
        :return: HttpResponse
        """

        ctx = {}
        return render(request, 'add/delete.html', ctx)

    def post(self, request):
        """
        Deletes user's profile picture

        :param request: ASGIRequest
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

        :param request: ASGIRequest
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

        :param request: ASGIRequest
        :param pk: int
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

        :param request: ASGIRequest
        :param pk: int
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

        :param request: ASGIRequest
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

        :param request: ASGIRequest
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

        :param request: ASGIRequest
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

        :param request: ASGIRequest
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






























class CreateChatView(LoginRequiredMixin, View):

    def get(self, request, pk):
        fm = ChatForm()
        op = get_object_or_404(User, pk=pk)
        sender = UserMessage.objects.filter(chat__sender=request.user, chat__receiver=op)
        receiver = UserMessage.objects.filter(chat__receiver=request.user, chat__sender=op)
        row = (sender | receiver)
        orderd_row = row.order_by('created_at')
        contx = {'form':fm, 'ordered_row':orderd_row}
        return render(request, 'user_profile/chat.html', contx)

    def post(self, request, pk):
        fm = ChatForm(request.POST)
        if fm.is_valid():
            c = fm.cleaned_data.get('chat')
            rev = get_object_or_404(User, pk=pk)
            owner_row, created = Chat.objects.get_or_create(sender=request.user, receiver=rev)
            row = UserMessage(text=c, chat=owner_row)
            row.save()
            return redirect(reverse('user_profile:chat', args=[rev.id]))
        contx = {'form':fm}
        return render(request, 'user_profile/chat.html', contx)

class ListChatView(LoginRequiredMixin, View):

    def get(self, request):
        sender = Chat.objects.filter(sender=request.user)
        receiver = Chat.objects.filter(receiver=request.user)
        orderd_row = sender | receiver
        contx = {'ordered_row':orderd_row}
        return render(request, 'user_profile/chat_list.html', contx)


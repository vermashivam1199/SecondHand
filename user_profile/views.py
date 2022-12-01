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

# Create your views here.

class UserProfileView(LoginRequiredMixin, View):
    sucess_url = reverse_lazy('add:add_list')

    def get(self, request):
        if 'pk' in request.session:
            del request.session['pk']

        u = get_object_or_404(User, pk=self.request.user.id)
        categories = Category.objects.all()
        if request.user.is_authenticated:
            fav = request.user.user_category_favrioute.values('id')
            favr = [f['id'] for f in fav]
        contx = {'owner':u, 'categories':categories, 'favrioute':favr}
        return render(request, 'user_profile/owner_home.html', contx)


class OwnerProfilePhotoUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        owner = request.user
        pic = get_object_or_404(OwnerProfilePhoto, owner=owner)
        fm = OwnerProfilePhotoForm(instance=pic)
        ctx = {'form':fm}
        return render(request, 'user_profile/profile_photo.html', ctx)

    def post(self, request):
        owner = request.user
        pic = get_object_or_404(OwnerProfilePhoto, owner=owner)
        fm = OwnerProfilePhotoForm(request.POST, request.FILES or None, instance=pic)
        if fm.is_valid():
            row = fm.save()
            return redirect(reverse('user_profile:profile_page'))
        ctx = {'form':fm}
        return render(request, 'user_profile/profile_photo.html', ctx)

def stream_profile_pic(request):
        pic = get_object_or_404(OwnerProfilePhoto, owner=request.user)
        pint(pic)
        response = HttpResponse()
        response['Content-Type'] = pic.content_type
        response['Content-Length'] = len(pic.picture)
        response.write(pic.picture)
        return response



class OwnerProfilePhotoDeleteView(LoginRequiredMixin, View):

    def get(self, request):
        ctx = {}
        return render(request, 'add/delete.html', ctx)

    def post(self, request):
        owner = request.user
        pic = get_object_or_404(OwnerProfilePhoto, owner=owner)
        fm = OwnerProfilePhotoForm(request.POST, request.FILES or None, instance=pic)
        if fm.is_valid():
            row = fm.save(commit=False)
            row.picture = None
            row.content_type = None
            row.save()
            return redirect(reverse('user_profile:profile_page'))
        ctx = {'form':fm}
        return render(request, 'add/delete.html', ctx)

class OwnerAboutView(View):

    def get(self, request, pk):

        owner = get_object_or_404(User, pk=pk)
        contx = {'owner':owner}
        return render(request, 'user_profile/owner_about.html', contx)




@method_decorator(csrf_exempt, name='dispatch')
class CreateFavriouteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        c = get_object_or_404(Category, pk=pk)
        sav = Favrioute(owner=request.user, category=c)
        try:
            sav.save()
        except IntegrityError:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavriouteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        c = get_object_or_404(Category, pk=pk)
        try:
            sav = Favrioute.objects.get(owner=request.user, category= c).delete()
        except Favrioute.DoesNotExist as e:
            pass
        return HttpResponse()

class UserUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        fm = UserUpdateForm(instance=request.user)
        contx = {'form':fm}
        return render(request, 'user_profile/user_update.html', contx)

    def post(self, request):
        fm = UserUpdateForm(request.POST, instance=request.user)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('user_profile:profile_page'))
        contx = {'form':fm}
        return render(request, 'user_profie/user_update.html', contx)



class PasswordUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        fm = PasswordChangeForm(user=request.user)
        contx = {'form':fm}
        return render(request, 'user_profile/user_update.html', contx)

    def post(self, request):
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


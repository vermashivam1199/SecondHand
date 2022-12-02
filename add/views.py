
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from add.tests import pint
from .models import (Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo, Feature)
from .forms import AddForm, PhotoForm, PhotoUpdateForm, CommentForm, OfferedPriceForm, FeatureForm
from django.urls import reverse_lazy, reverse
from .owner import OwnerDeleteView
from django import forms

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


# Create your views here.



# Add
# <----------------------------------------------------------------------------------------------------->
class AddListView(View):

    def get(self,request):
        adds = Add.objects.all()
        saved = list()
        if request.user.is_authenticated:
            sav = request.user.user_add_saved.values('id')
            saved = [s['id'] for s in sav]
        context = {'adds':adds, 'saved':saved}
        return render(request,'add/list.html',context)

class AddCreateView(LoginRequiredMixin, View):
    sucess_url = reverse_lazy('add:add_photo')

    def get(self, request):
        if 'pk' in request.session:
            pk = request.session['pk']
            a = get_object_or_404(Add, pk=pk, owner=self.request.user)
            fm = AddForm(instance=a)
        else:
            fm = AddForm()
        contx = {'form':fm}
        return render(request, 'add/add_create.html', contx)

    def post(self,request):
        if 'pk' in request.session:
            pk = request.session['pk']
            a = get_object_or_404(Add, pk=pk, owner=self.request.user)
            fm = AddForm(request.POST, instance=a)
        else:
            fm = AddForm(request.POST)
        if fm.is_valid():
            row = fm.save(commit=False)
            row.owner = request.user
            row.save()
            request.session['pk'] = row.pk
            return redirect(self.sucess_url)
        contx = {'form':fm}
        return render(request, 'add/add_create.html', contx)


class AddDetailView(View):

    def get(self, request, id):
        add = get_object_or_404(Add, pk=id)
        comments = Comment.objects.filter(add=add.id)
        comment_fm = CommentForm()
        offered_price_fm = OfferedPriceForm()
        offered_price = OfferedPrice.objects.filter(add=add.id, owner=request.user.id)
        if offered_price:
            offered_price_fm = OfferedPriceForm(instance=offered_price[0])
        pic = add.add_photo.all()
        features = Feature.objects.filter(add=add.id)
        contx = {
            'add':add, 'picture':pic, 'comments':comments, 'comment_fm':comment_fm, 'offered_price_fm':offered_price_fm, 'features':features
        }
        return render(request, 'add/detail.html', contx)


class AddUpdateView(LoginRequiredMixin, View):

    def get(self, request, id):
        row = get_object_or_404(Add, pk=id, owner=self.request.user)
        fm = AddForm(instance=row)
        contx = {'form':fm, 'row':row.id}
        return render(request, 'add/add_update.html', contx)
    
    def post(self, request, id):
        row = get_object_or_404(Add, pk=id, owner=self.request.user)
        fm = AddForm(request.POST, instance=row)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('add:owner_detail', args=[row.id]))
        contx = {'form':fm, 'row':row.id}
        return render(request, 'add/add_update.html', contx)

def stream_file(request, id):
        pic = get_object_or_404(Photo, pk=id)
        response = HttpResponse()
        if pic.content_type:
            response['Content-Type'] = pic.content_type
            response['Content-Length'] = len(pic.picture)
            response.write(pic.picture)
        return response

class AddDeleteView(OwnerDeleteView):
    model = Add
    success_url = reverse_lazy('add:owner_list')
    template_name = 'add/delete.html'
# <----------------------------------------------------------------------------------------------------->




# Owner
# <----------------------------------------------------------------------------------------------------->
class OwnerListView(LoginRequiredMixin, View):

    def get(self,request):
        adds = Add.objects.filter(owner=self.request.user)
        context = {'adds':adds}
        return render(request,'add/owner_list.html',context)


class OwnerDetailView(LoginRequiredMixin, View):

    def get(self, request, id):
        add = get_object_or_404(Add, pk=id, owner=self.request.user)
        pic = add.add_photo.all()
        fm = FeatureForm()
        features = Feature.objects.filter(add=add.id)
        contx = {'add':add, 'picture':pic, 'form':fm, 'features':features}
        return render(request, 'add/owner_detail.html', contx)
# <----------------------------------------------------------------------------------------------------->




# Photo
# <----------------------------------------------------------------------------------------------------->
class PhotoCreateView(LoginRequiredMixin, View):
    sucess_url = reverse_lazy('user_profile:profile_page')
    home_url = reverse_lazy('home:all')

    def get(self, request):
        fm = PhotoForm()
        contx = {'form':fm}
        return render(request, 'add/add_photo.html', contx)

    def post(self,request):
        files = request.FILES.getlist('picture')
        files_len = len(files)
        res = redirect(self.sucess_url)
        if 'pk' in request.session:
                pk = request.session['pk']
                a = get_object_or_404(Add, pk=pk)
                pic = Photo.objects.filter(add=a.id)
                photo_l = str(len(pic))
        else:
            raise forms.ValidationError('no add found')
        for file in files:
            fm = PhotoForm(request.POST, request.FILES or None, photo_list=photo_l, current_pic=files_len)
            if fm.is_valid():
                row = fm.save(file, commit=False)
                row.add = a
                row.save()
                res = redirect(self.sucess_url)
            else:
                contx = {'form':fm}
                return render(request, 'add/add_photo.html', contx)
        return res


class PhotoUpdateView(LoginRequiredMixin, View):

    def get(self, request, pic_id, add_id):
        a = get_object_or_404(Add, pk=add_id, owner=self.request.user)
        row = get_object_or_404(Photo, pk=pic_id, add=a)
        fm = PhotoUpdateForm(instance=row)
        contx = {'form':fm, 'row':row.add.id}
        return render(request, 'add/photo_update.html', contx)
    
    def post(self, request, pic_id, add_id):
        a = get_object_or_404(Add, pk=add_id, owner=self.request.user)
        row = get_object_or_404(Photo, pk=pic_id, add=a)
        fm = PhotoUpdateForm(request.POST, request.FILES or None, instance=row)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('add:owner_detail', args=[a.id]))
        contx = {'form':fm, 'row':row.add.id}
        return render(request, 'add/photo_update.html', contx)


class PhotoAddView(LoginRequiredMixin, View):

    def get(self, request, add_id):
        a = get_object_or_404(Add, pk=add_id, owner=self.request.user)
        fm = PhotoForm()
        contx = {'form':fm, 'row':a.id}
        return render(request, 'add/add_photo.html', contx)

    def post(self,request, add_id):
        files = request.FILES.getlist('picture')
        res = None
        a = get_object_or_404(Add, pk=add_id, owner=self.request.user)
        pic = Photo.objects.filter(add=a.id)
        photo_l = str(len(pic))
        for file in files:
            fm = PhotoForm(request.POST, request.FILES or None, photo_list=photo_l, current_pic=len(files))
            if fm.is_valid():
                row = fm.save(file, commit=False)
                row.add = a
                row.save()
                res = redirect(reverse('add:owner_detail', args=[a.id]))
            else:
                contx = {'form':fm}
                return render(request, 'add/add_photo.html', contx)

        if res:
            return res
        else:
            raise forms.ValidationError('you need to add a photo')


class PhotoDeleteView(LoginRequiredMixin, View):

    def get(self,request, pk):
        return render(request, 'add/delete.html', {})

    def post(self, request, pk):
        pic = get_object_or_404(Photo, pk=pk)
        if pic.add.owner == self.request.user:
            pic.delete()
            return redirect(reverse('add:owner_detail', args=[pic.add.id]))
        raise forms.ValidationError('you are not the user')
# <----------------------------------------------------------------------------------------------------->





# Comment
# <----------------------------------------------------------------------------------------------------->
class CommentView(LoginRequiredMixin, View):

    def post(self, request, pk):
        a = Add(pk=pk)
        fm = CommentForm(request.POST)
        if fm.is_valid():
            pint(fm.cleaned_data)
            row = fm.save(commit=False)
            row.owner = request.user
            row.add = a
            row.save()
            return redirect(reverse('add:add_detail', args=[a.id]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = 'add/delete.html'

    def get_success_url(self):
        a = self.object.add
        pint(a.id)
        pint(type(a.id))
        return reverse('add:add_detail', args=[a.id])
# <----------------------------------------------------------------------------------------------------->





# Saved
# <----------------------------------------------------------------------------------------------------->
@method_decorator(csrf_exempt, name='dispatch')
class CreateSavedView(LoginRequiredMixin, View):

    def post(self, request, pk):
        a = get_object_or_404(Add, pk=pk)
        sav = Saved(owner=request.user, add=a)
        try:
            sav.save()
        except IntegrityError:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteSavedView(LoginRequiredMixin, View):

    def post(self, request, pk):
        a = get_object_or_404(Add, pk=pk)
        try:
            sav = Saved.objects.get(owner=request.user, add= a).delete()
        except Saved.DoesNotExist as e:
            pass
        return HttpResponse()
# <----------------------------------------------------------------------------------------------------->





# Offered Price
# <----------------------------------------------------------------------------------------------------->
class OfferedPriceView(LoginRequiredMixin, View):

    def post(self, request, pk):
        a = get_object_or_404(Add, pk=pk)
        fm = OfferedPriceForm(request.POST)
        try:
            if fm.is_valid():
                row = fm.save(commit=False)
                row.add = a
                row.owner = request.user
                row.save()
                return redirect(reverse('add:add_detail', args=[a.id]))
            contx = {'form':fm}
            return render(request, 'add/add_photo.html', contx)

        except (IntegrityError):
            op = OfferedPrice.objects.get(add=a.id, owner=request.user.id)
            fm = OfferedPriceForm(request.POST, instance=op)
            if fm.is_valid():
                row = fm.save(commit=False)
                row.add = a
                row.owner = request.user
                row.save()
                return redirect(reverse('add:add_detail', args=[a.id]))
            contx = {'form':fm}
            return render(request, 'add/add_photo.html', contx)

       
class OfferedPriceDelete(LoginRequiredMixin, View):

    def post(self, request, pk):
        a = get_object_or_404(Add, pk=pk)
        o = get_object_or_404(OfferedPrice, owner=request.user, add=a)
        o.delete()
        return redirect(reverse('add:add_detail', args=[a.id]))
# <----------------------------------------------------------------------------------------------------->




# Feature
# <----------------------------------------------------------------------------------------------------->
class FeatureView(LoginRequiredMixin, View):

    def post(self, request, pk):
        a = get_object_or_404(Add, pk=pk, owner=request.user.id)
        fm = FeatureForm(request.POST, add_id=a.id)
        if fm.is_valid():
            row = fm.save(commit=False)
            row.add = a
            row.save()
            return redirect(reverse('add:owner_detail', args=[a.id]))
        messages.add_message(request, messages.INFO, 'can only save 15 features')
        return redirect(reverse('add:owner_detail', args=[a.id]))

class FeatureUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        a = get_object_or_404(Add, owner=request.user.id)
        f = get_object_or_404(Feature, pk=pk, add=a.id)
        fm = FeatureForm(instance=f)
        contx = {'form':fm, 'row':a.id}
        return render(request, 'add/add_update.html', contx)

    def post(self, request, pk):
        a = get_object_or_404(Add, owner=request.user.id)
        f = get_object_or_404(Feature, pk=pk, add=a.id)
        fm = FeatureForm(request.POST, instance=f)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('add:owner_detail', args=[a.id]))
        messages.add_message(request, messages.INFO, 'can only save 15 features')
        return redirect(reverse('add:owner_detail', args=[a.id]))


class FeatureDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        a = get_object_or_404(Add, owner=request.user.id)
        f = get_object_or_404(Feature, pk=pk, add=a.id)
        pint('working1')
        f.delete()
        pint('working')
        return redirect(reverse('add:owner_detail', args=[a.id]))
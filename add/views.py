
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

import asyncio
from asgiref.sync import sync_to_async



# Create your views here.



# Add
# <----------------------------------------------------------------------------------------------------->
class AddListView(View):
    """This view displays list of adds"""

    def get(self,request):
        """
        Displays QuerySet of Add objects

        :param ASGIRequest request: Request object
        :context: 
            adds: QuerySet of Add objects
            saved: QuerySet of Saved objects
        :return: HttpResponse
        """

        adds = Add.objects.all()
        saved = list()
        if request.user.is_authenticated:
            sav = request.user.user_add_saved.values('id') # returns list of Saved Adds in form of dict objects
            saved = [s['id'] for s in sav] # creating a list of Saved IDs that user has Saved
        context = {'adds':adds, 'saved':saved}
        return render(request,'add/list.html',context)


class AddCreateView(LoginRequiredMixin, View):
    """A view to create new adds"""

    sucess_url = reverse_lazy('add:add_photo')

    def get(self, request):
        """
        Displays AddForm 

        If user returns to this view without completing the whole Add creation process
        this view will display the same add in AddForm the user didn't completed.

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class AddForm
        :return: HttpResponse
        """

        if 'pk' in request.session:
            pk = request.session['pk']
            a = get_object_or_404(Add, pk=pk, owner=self.request.user)
            fm = AddForm(instance=a)
        else:
            fm = AddForm()
        contx = {'form':fm}
        return render(request, 'add/add_create.html', contx)

    def post(self,request):
        """
        Creates new Add 

        Creating session to save the user's ongoing progress of Add creation

        :param ASGIRequest request: Request object
        :context: 
            form: An instance of form class AddForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        if 'pk' in request.session:
            pk = request.session['pk']
            a = get_object_or_404(Add, pk=pk, owner=self.request.user) # creating add object from add id stored in session
            fm = AddForm(request.POST, instance=a)
        else:
            fm = AddForm(request.POST)
        if fm.is_valid():
            row = fm.save(commit=False)
            row.owner = request.user
            row.save()
            request.session['pk'] = row.pk # saving current add's id in session
            return redirect(self.sucess_url)
        contx = {'form':fm}
        return render(request, 'add/add_create.html', contx)


class AddDetailView(View):
    """A view to display detail page of an add"""

    @sync_to_async(thread_sensitive=False)
    def helper_comment(self, add):
        """A helper method that returns list of Comment objects through sync_to_async decorator"""

        com = Comment.objects.filter(add=add.id)
        return list(com)
    
    @sync_to_async(thread_sensitive=False)
    def helper_offered_price(self, add):
        """A helper method that returns list of OfferedPrice object through sync_to_async decorator"""   

        op = OfferedPrice.objects.filter(add=add.id, owner=self.request.user.id)
        return list(op)

    @sync_to_async(thread_sensitive=False)
    def helper_pic(self, add):
        """A helper method that returns list of photos object through sync_to_async decorator"""   

        p = add.add_photo.all()
        return list(p)

    @sync_to_async(thread_sensitive=False)
    def helper_features(self, add):
        """A helper method that returns list of OfferedPrice object through sync_to_async decorator"""   

        f = Feature.objects.filter(add=add.id)
        return list(f)
    
    @sync_to_async
    def helper_render(self, contx):
        """A helper method that returns render function by calling through sync_to_async decorator"""   

        return render(self.request, 'add/detail.html', contx)



    async def get(self, request, pk):
        """
        Displays deatil page of an add 

        :param ASGIRequest request: Request object
        :param int pk: primary key of Add tabel
        :context:
            add: Instance of model class Add
            comments: List of instance of model class Comment
            comment_fm: An instance of form class CommentForm
            offered_price_fm: An instance of form class OfferedPriceForm
            features: List of instance of model class Feature
        :return: HttpResponse
        """

        add = await sync_to_async(get_object_or_404)(Add, pk=pk)
        comments, offered_price, pic, features = await asyncio.gather(
            self.helper_comment(add), self.helper_offered_price(add), self.helper_pic(add), self.helper_features(add)
        )
        comment_fm = CommentForm()
        offered_price_fm = OfferedPriceForm()
        if offered_price: # checking if current user has already offered price to the current add
            offered_price_fm = OfferedPriceForm(instance=offered_price[0])
        contx = {
            'add':add, 'picture':pic, 'comments':comments, 'comment_fm':comment_fm, 'offered_price_fm':offered_price_fm, 'features':features
        }
        return await self.helper_render(contx)



class AddUpdateView(LoginRequiredMixin, View):
    """This view update Add"""

    def get(self, request, pk):
        """
        Displays AddForm

        :param ASGIRequest request: Request object
        :param int pk: primary key of Add tabel
        :context:
            row: Primary key of model class Add 
            form: An instance of form class AddForm
        :return: HttpResponse
        """

        row = get_object_or_404(Add, pk=pk, owner=self.request.user)
        fm = AddForm(instance=row)
        contx = {'form':fm, 'row':row.id}
        return render(request, 'add/add_update.html', contx)
    
    def post(self, request, pk):
        """
        Updates Add

        :param ASGIRequest request: Request object
        :param int pk: primary key of Add tabel
        :context:
            row: Primary key of model class Add 
            form: An instance of form class AddForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        row = get_object_or_404(Add, pk=pk, owner=self.request.user)
        fm = AddForm(request.POST, instance=row)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('add:owner_detail', args=[row.id]))
        contx = {'form':fm, 'row':row.id}
        return render(request, 'add/add_update.html', contx)



@sync_to_async(thread_sensitive=False)
def stream_file(request, pk):
    """
    This view sends instance of Photo class

    :param ASGIRequest request: Request object
    :param int pk: primary key of Photo tabel
    :return: HttpResponse
    """

    pic = get_object_or_404(Photo, pk=pk)
    response = HttpResponse()
    if pic.content_type:
        response['Content-Type'] = pic.content_type
        response['Content-Length'] = len(pic.picture)
        response.write(pic.picture)
    return response


class AddDeleteView(OwnerDeleteView):
    """This view deletes Add"""

    model = Add
    success_url = reverse_lazy('add:owner_list')
    template_name = 'add/delete.html'
# <----------------------------------------------------------------------------------------------------->




# Owner
# <----------------------------------------------------------------------------------------------------->
class OwnerListView(LoginRequiredMixin, View):
    """This view displays list of adds created by the current user"""

    def get(self,request):
        """
        Displays QuerySet of Add objects created by current user

        :param ASGIRequest request: Request object
        :context: 
            adds: QuerySet of Add objects
        :return: HttpResponse
        """

        adds = Add.objects.filter(owner=self.request.user)
        context = {'adds':adds}
        return render(request,'add/owner_list.html',context)


class OwnerDetailView(LoginRequiredMixin, View):
    """A view to display detail page of an add created by current user"""

    @sync_to_async(thread_sensitive=False)
    def helper_pic(self, add):
        """A helper method that returns list of photos object through sync_to_async decorator"""   

        p = add.add_photo.all()
        return list(p)

    @sync_to_async(thread_sensitive=False)
    def helper_features(self, add):
        """A helper method that returns list of OfferedPrice object through sync_to_async decorator"""   

        f = Feature.objects.filter(add=add.id)
        return list(f)
    
    @sync_to_async
    def helper_render(self, contx):
        """A helper method that returns render function by calling through sync_to_async decorator"""   

        return render(self.request, 'add/owner_detail.html', contx)

    async def get(self, request, pk):
        """
        Displays deatil page of an add  created by current user

        :param ASGIRequest request: Request object
        :param int pk: primary key of Add tabel
        :context:
            add: Instance of model class Add
            picture: Instance of model class Photo
            features: List of instance of model class Feature
        :return: HttpResponse
        """

        add = await sync_to_async(get_object_or_404, thread_sensitive=False)(Add, pk=pk, owner=self.request.user)
        pic, features = await asyncio.gather(self.helper_pic(add), self.helper_features(add))
        fm = FeatureForm()
        contx = {'add':add, 'picture':pic, 'form':fm, 'features':features}
        return await self.helper_render(contx)
# <----------------------------------------------------------------------------------------------------->




# Photo
# <----------------------------------------------------------------------------------------------------->
class PhotoCreateView(LoginRequiredMixin, View):
    """
    This view creates Photo of current add
    
    Works with AddCreateView
    """

    sucess_url = reverse_lazy('user_profile:profile_page')
    home_url = reverse_lazy('home:all')

    def get(self, request):
        """
        Displays PhotoForm

        :param request: ASGIRequest
        :context: 
            form: PhotoForm
        :return: HttpResponse
        """

        fm = PhotoForm()
        contx = {'form':fm}
        return render(request, 'add/add_photo.html', contx)

    def post(self,request):
        """
        Creates Photo for current add

        :param ASGIRequest request: Request object
        :context: 
            form: PhotoForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        files = request.FILES.getlist('picture') # list of multiple photos got from PhotoForm
        files_len = len(files) # number of photos send thru request
        res = redirect(self.sucess_url)
        if 'pk' in request.session: # this 'pk'(primary key) session allows backend to know the current instance of Add
                pk = request.session['pk']
                a = get_object_or_404(Add, pk=pk) # Gets Add object by using Add primary key from session
        else: # if there is no 'pk'(primary key) in the session then you won't be able to save photo
            raise forms.ValidationError('no add found')
        for file in files:
            pic = Photo.objects.filter(add=a.id) # Gets current Photo objects associated with current Add
            photo_l = str(len(pic)) # get total number of photos of current add saved in database
            fm = PhotoForm(request.POST, request.FILES or None, photo_list=photo_l, current_pic=files_len) # Calling PhotoForm constructer with additional arguments
            if fm.is_valid():
                row = fm.save(file, commit=False)
                row.add = a
                row.save()
                res = redirect(self.sucess_url)
                files_len -= 1 # subtracting the current pics left
            else:
                contx = {'form':fm}
                return render(request, 'add/add_photo.html', contx)
        return res


class PhotoUpdateView(LoginRequiredMixin, View):
    """This view is to update the photo"""

    def get(self, request, pic_id, add_id):
        """
        Displays PhotoUpdateForm

        :param ASGIRequest request: Request object
        :param int pic_id: Primary key of Photo table
        :param int add_id: Primary key of Add table
        :context: 
            form: PhotoUpdateForm
            row: Primary key of current Add instance
        :return: HttpResponse
        """

        a = get_object_or_404(Add, pk=add_id, owner=self.request.user)
        row = get_object_or_404(Photo, pk=pic_id, add=a)
        fm = PhotoUpdateForm(instance=row)
        contx = {'form':fm, 'row':row.add.id}
        return render(request, 'add/photo_update.html', contx)
    
    def post(self, request, pic_id, add_id):
        """
        Update Photo for current add

        :param ASGIRequest request: Request object
        :param int pic_id: Primary key of Photo table
        :param int add_id: Primary key of Add table
        :context: 
            form: PhotoUpdateForm
            row: Primary key of current Add instance
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        a = get_object_or_404(Add, pk=add_id, owner=self.request.user)
        row = get_object_or_404(Photo, pk=pic_id, add=a)
        fm = PhotoUpdateForm(request.POST, request.FILES or None, instance=row)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('add:owner_detail', args=[a.id]))
        contx = {'form':fm, 'row':row.add.id}
        return render(request, 'add/photo_update.html', contx)


class PhotoAddView(LoginRequiredMixin, View):
    """This view is to add additional Photo to an Add"""

    def get(self, request, add_id):
        """
        Displays PhotoForm

        :param ASGIRequest request: Request object
        :param int add_id: Primary key of Add table
        :context: 
            form: PhotoUpdateForm
            row: Primary key of current Add instance
        :return: HttpResponse
        """

        a = get_object_or_404(Add, pk=add_id, owner=self.request.user)
        fm = PhotoForm()
        contx = {'form':fm, 'row':a.id}
        return render(request, 'add/add_photo.html', contx)

    def post(self,request, add_id):
        """
        Add Photo for current add

        :param ASGIRequest request: Request object
        :param int add_id: Primary key of Add table
        :context: 
            form: PhotoForm
            row: Primary key of current Add instance
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        files = request.FILES.getlist('picture') # list of multiple photos got from PhotoForm
        file_l = len(files) # number of photos send thru request
        res = None
        a = get_object_or_404(Add, pk=add_id, owner=self.request.user)
        res = redirect(reverse('add:owner_detail', args=[a.id]))
        
        for file in files:
            pic = Photo.objects.filter(add=a.id) # Gets current Photo objects associated with current Add
            photo_l = str(len(pic)) # get total number of photos of current add saved in database
            fm = PhotoForm(request.POST, request.FILES or None, photo_list=photo_l, current_pic=file_l) # Calling PhotoForm constructer with additional arguments
            if fm.is_valid():
                row = fm.save(file, commit=False)
                row.add = a 
                row.save()
                res = redirect(reverse('add:owner_detail', args=[a.id]))
                file_l -= 1 # subtracting the current pics left
            else:
                contx = {'form':fm}
                return render(request, 'add/add_photo.html', contx)
        return res


class PhotoDeleteView(LoginRequiredMixin, View):
    """This view is to delete Photos"""

    def get(self,request, pk):
        """
        Displays form

        :param ASGIRequest request: Request object
        :param int pk: Primary key of Photo table
        :return: HttpResponse
        """

        return render(request, 'add/delete.html', {})

    def post(self, request, pk):
        """
        Deletes Photo

        :param ASGIRequest request: Request object
        :param int pk: Primary key of Photo table
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

        pic = get_object_or_404(Photo, pk=pk)
        if pic.add.owner == self.request.user:
            pic.delete()
            return redirect(reverse('add:owner_detail', args=[pic.add.id]))
        raise forms.ValidationError('you are not the user')
# <----------------------------------------------------------------------------------------------------->





# Comment
# <----------------------------------------------------------------------------------------------------->
class CommentView(LoginRequiredMixin, View):
    """This view is to add a new comment to an Add"""

    def post(self, request, pk):
        """
        Add Photo for current add

        :param ASGIRequest request: Request object
        :param int add_id: Primary key of Add table
        :return: HttpResponseRedirect
        """
        a = Add(pk=pk)
        fm = CommentForm(request.POST)
        if fm.is_valid():
            row = fm.save(commit=False)
            row.owner = request.user
            row.add = a
            row.save()
            return redirect(reverse('add:add_detail', args=[a.id]))
        return redirect(reverse('add:add_detail', args=[a.id]))


class CommentDeleteView(OwnerDeleteView):
    """This view is to delete comment"""
    
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
    """This view is to record the saved adds of current user"""

    def post(self, request, pk):
        """
        Record the saved adds of current user

        :param ASGIRequest request: Request object
        :param int add_id: Primary key of Add table
        :return: HttpResponse
        """
        
        a = get_object_or_404(Add, pk=pk)
        sav = Saved(owner=request.user, add=a)
        try:
            sav.save()
        except IntegrityError: # If the add is alerady saved
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteSavedView(LoginRequiredMixin, View):
    """Delete Saved adds of current video"""

    def post(self, request, pk):
        """
        Delete the saved adds of current user

        :param ASGIRequest request: Request object
        :param int add_id: Primary key of Add table
        :return: HttpResponse
        """
        a = get_object_or_404(Add, pk=pk)
        try:
            Saved.objects.get(owner=request.user, add= a).delete()
        except Saved.DoesNotExist as e:
            pass
        return HttpResponse()
# <----------------------------------------------------------------------------------------------------->





# Offered Price
# <----------------------------------------------------------------------------------------------------->
class OfferedPriceView(LoginRequiredMixin, View):
    """This view is to save the price offered by user to an Add"""

    def post(self, request, pk):
        """
        Saves instance of OfferedPrice model class

        If the current user has already offered price to the current add, 
        then in that case it will updates the OfferedPrice instance related to that add

        :param ASGIRequest request: Request object
        :param int add_id: Primary key of Add table
        :context: 
            form: OfferedPriceForm
        :return if form valid: HttpResponseRedirect
        :return if form not valid: HttpResponse
        """

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
    """This view deletes the price offered by current user on an add"""

    def post(self, request, pk):
        """
        Saves instance of OfferedPrice model class

        If the current user has already offered price to the current add, 
        then in that case it will updates the OfferedPrice instance related to that add

        :param ASGIRequest request: Request object
        :param int add_id: Primary key of Add table
        :return: HttpResponseRedirect
        """

        a = get_object_or_404(Add, pk=pk)
        o = get_object_or_404(OfferedPrice, owner=request.user, add=a)
        o.delete()
        return redirect(reverse('add:add_detail', args=[a.id]))
# <----------------------------------------------------------------------------------------------------->




# Feature
# <----------------------------------------------------------------------------------------------------->
class FeatureView(LoginRequiredMixin, View):
    """This view lets user add features to their add"""

    def post(self, request, pk):
        """
        Saves instance of Feature model class

        :param ASGIRequest request: Request object
        :param int pk: Primary key of Add table
        :context: 
            form: PhotoUpdateForm
        :return: HttpResponseRedirect
        """
        
        a = get_object_or_404(Add, pk=pk, owner=request.user.id)
        fm = FeatureForm(request.POST, add_id=a.id)# Calling FeatureForm constructer with additional arguments
        if fm.is_valid():
            row = fm.save(commit=False)
            row.add = a
            row.save()
            return redirect(reverse('add:owner_detail', args=[a.id]))
        messages.add_message(request, messages.INFO, 'can only save 15 features')
        return redirect(reverse('add:owner_detail', args=[a.id]))

class FeatureUpdateView(LoginRequiredMixin, View):
    """This view lets user update features to their add"""


    def get(self, request, pk):
        """
        Displays FeatureForm

        :param ASGIRequest request: Request object
        :param int pk: Primary key of Add table
        :context: 
            form: FeatureForm
        :return: HttpResponse
        """

        a = get_object_or_404(Add, owner=request.user.id)
        f = get_object_or_404(Feature, pk=pk, add=a.id)
        fm = FeatureForm(instance=f)
        contx = {'form':fm, 'row':a.id}
        return render(request, 'add/add_update.html', contx)

    def post(self, request, pk):
        """
        Updates instance of Feature model class

        :param ASGIRequest request: Request object
        :param int pk: Primary key of Add table
        :context: 
            form: FeatureForm
        :return: HttpResponseRedirect
        """

        a = get_object_or_404(Add, owner=request.user.id)
        f = get_object_or_404(Feature, pk=pk, add=a.id)
        fm = FeatureForm(request.POST, instance=f)
        if fm.is_valid():
            fm.save()
            return redirect(reverse('add:owner_detail', args=[a.id]))
        messages.add_message(request, messages.INFO, 'can only save 15 features')
        return redirect(reverse('add:owner_detail', args=[a.id]))


class FeatureDeleteView(LoginRequiredMixin, View):
    """This view deletes feture of current add"""

    def post(self, request, pk_feature, pk_add):
        """
        Delete the feature of current add
        :param ASGIRequest request: Request object
        :param int pk_add: Primary key of Add table
        :param int pk_feature: Primary key of Feature table
        :return: HttpResponse
        """

        a = get_object_or_404(Add, pk=pk_add, owner=request.user.id)
        f = get_object_or_404(Feature, pk=pk_feature, add=a.id)
        f.delete()
        return redirect(reverse('add:owner_detail', args=[a.id]))
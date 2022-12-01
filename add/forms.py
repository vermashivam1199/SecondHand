from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Add, Photo, Comment, OfferedPrice, Feature
from .humanise import naturalsize
from .tests import pint
from django.shortcuts import render, redirect, get_object_or_404

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

class AddForm(forms.ModelForm):
    class Meta:
        model = Add
        fields = ['name', 'description', 'price', 'category', 'tag']

class PhotoForm(forms.ModelForm):
    max_upload_limit = 5 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)
    max_photo_upload_limit = 5

    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    upload_field_name = 'picture'

    class Meta:
        model = Photo
        fields = ['picture' ]

    def __init__(self, *args, **kwargs):

        pint(kwargs.get('photo_list'))
        if kwargs.get('photo_list'):
            pint('init working')
            self.photo_list = kwargs.pop('photo_list')
        else:
            pint('else init working')
            self.photo_list = 0
        if kwargs.get('current_pic'):
            self.current_pic = kwargs.pop('current_pic')
        else:
            self.current_pic = None
        super(PhotoForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if self.photo_list and self.current_pic:
           
            pint('total----',int(self.photo_list) + int(self.current_pic))
            if int(self.photo_list) + int(self.current_pic) > 5:
                pint('if working')
                self.add_error('picture', f'max pics is 5')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', f'file must be less than {self.max_upload_limit_text}')

    def save(self, f=None, commit=True):
        instance = super(PhotoForm, self).save(commit=False)
        if isinstance(f, InMemoryUploadedFile) or isinstance(f, TemporaryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr
        if commit:
            instance.save()
        return instance

    def max_photo_length(self, id):
        add = get_object_or_404(Add, pk=id)
        photo_list = Photo.objects.filter(add=id)
        if len(photo_list)+1 > self.max_photo_upload_limit:
            raise forms.ValidationError({'picture':[f'max photo limit reached, you can only upload {self.max_photo_upload_limit} photos']})


class AddForm(forms.ModelForm):
    class Meta:
        model = Add
        fields = ['name', 'description', 'price', 'category', 'tag']

class PhotoUpdateForm(forms.ModelForm):
    max_upload_limit = 5 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Photo
        fields = ['picture' ]

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', f'file must be less than {self.max_upload_limit_text}')

    def save(self, commit=True):
        instance = super(PhotoUpdateForm, self).save(commit=False)
        f = instance.picture
        if isinstance(f, InMemoryUploadedFile) or isinstance(f, TemporaryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):  
    class Meta:
        model = Comment
        fields = ['text']


class OfferedPriceForm(forms.ModelForm):
    class Meta:
        model = OfferedPrice
        fields = ['price_offered' ]

class FeatureForm(forms.ModelForm):
    max_feature_limit = 15
    def __init__(self, *args, **kwargs):

        if kwargs.get('add_id'):
            self.add_id = kwargs.pop('add_id')
        else:
            self.add_idt = 0
        super(FeatureForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.add_id:
            feature = Feature.objects.filter(add=self.add_id)
            if len(feature) + 1 > self.max_feature_limit:
                raise forms.ValidationError({'feature':[f'max feature limit reached, you can only upload f{self.max_feature_limit} features']})


    class Meta:
        model = Feature
        fields = ['feature_name', 'feature']
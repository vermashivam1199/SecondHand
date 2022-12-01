from django.contrib.auth.models import User
from .models import OwnerProfilePhoto
from django import forms
from add.humanise import naturalsize
from add.tests import pint
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm



class OwnerProfilePhotoForm(forms.ModelForm):
    max_upload_limit = 5 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = OwnerProfilePhoto
        fields = ['picture' ]

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        pint(pic)
        pint('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            pint('error')
            self.add_error('picture', f'file must be less than {self.max_upload_limit_text}')

    def save(self, commit=True):
        instance = super(OwnerProfilePhotoForm, self).save(commit=False)
        f = instance.picture
        pint('in save')
        if isinstance(f, InMemoryUploadedFile) or isinstance(f, TemporaryUploadedFile):
            pint('is instance working')
            pint(f.content_type)
            bytrarr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytrarr
        if commit:
            instance.save()
        return instance


class ChatForm(forms.Form):
    chat = forms.CharField(max_length=256)

class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
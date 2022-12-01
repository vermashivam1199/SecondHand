from email.policy import default
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from .managers import RecemondationManager


class Category(models.Model):
    name = models.CharField(max_length=70)
    favrioute = models.ManyToManyField(User, through='Favrioute', related_name='user_category_favrioute')

    objects = models.Manager()
    recemondation = RecemondationManager()

    def __str__(self) -> str:
        return self.name

class Favrioute(models.Model):
    category = models.ForeignKey('Category',on_delete=models.CASCADE, related_name='category_favrioute')
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_favrioute')

    def __str__(self) -> str:
        return f'{self.owner.username} -> {self.category.name}' 

    class Meta:
        unique_together =   ('category','owner')


class Tag(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self) -> str:
        return self.name

class OfferedPrice(models.Model):
    price_offered = models.DecimalField(max_digits=10, decimal_places=2)
    add = models.ForeignKey('Add',on_delete=models.CASCADE, related_name='add_offered_price')
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_offered_price')

    def __str__(self) -> str:
        return str(self.price_offered)

    class Meta:
        unique_together =   ('add','owner')

class Saved(models.Model):
    add = models.ForeignKey('Add',on_delete=models.CASCADE, related_name='add_saved')
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_saved')

    def __str__(self) -> str:
        return self.owner.username

    class Meta:
        unique_together =   ('add','owner')

class History(models.Model):
    text = models.CharField(max_length=256)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_history')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.owner.username

class ReportCategory(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self) -> str:
        return self.name

class Report(models.Model):
    add = models.ForeignKey('Add',on_delete=models.CASCADE, related_name='add_report')
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_report')
    cause = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    report_category = models.ForeignKey('ReportCategory',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.report_category.name

class Comment(models.Model):
    add = models.ForeignKey('Add',on_delete=models.CASCADE, related_name='add_comment')
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_comment')
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.owner.username

class Add(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    counter = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_add')
    tag = models.ManyToManyField('Tag', blank=True)
    offered_price = models.ManyToManyField(User, through='OfferedPrice', related_name='user_add_offered_price')
    saved = models.ManyToManyField(User, through='Saved', related_name='user_add_saved')
    report = models.ManyToManyField(User, through='Report', related_name='user_add_report')
    comment = models.ManyToManyField(User, through='Comment', related_name='user_add_comment')

    def __str__(self) -> str:
        return self.name

class Photo(models.Model):
    picture = models.BinaryField(null=False, editable=True, blank=False)
    content_type = models.CharField(max_length=256, null=False, help_text='The MIMEType of the file', blank=False)
    add = models.ForeignKey('Add', on_delete=models.CASCADE, related_name='add_photo')

    def __str__(self) -> str:
        return self.add.name

class Feature(models.Model):
    feature_name = models.CharField(max_length=256, null=False)
    feature = models.CharField(max_length=256, null=False)
    add = models.ForeignKey('Add', on_delete=models.CASCADE, related_name='add_feature')

    def __str__(self) -> str:
        return self.add.name
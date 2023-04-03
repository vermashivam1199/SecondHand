from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from user_profile.models import OwnerProfilePhoto
from add.tests import pint
from add.models import (Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo, Favrioute)
from django.db.models import Count
import asyncio
from django.core.handlers.asgi import ASGIRequest
from secondhand.tasks import test_funk
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import NotificationModel

# Create your views here.

class NotificationListView(LoginRequiredMixin, View):

    def get(self, request):
        notifications = NotificationModel.objects.filter(receiver=request.user)
        contx = {"notifications":notifications}
        return render(request, "notification/notification_list.html", contx)
    
class NotificationDetail(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        row = get_object_or_404(NotificationModel, pk=pk)
        row.seen = True
        row.save()
        contx = {"notification": row}
        return render(request, "notification/notification_deatil.html", contx)
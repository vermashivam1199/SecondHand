from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from add.tests import pint
from django.urls import reverse_lazy, reverse
from django import forms
import json
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
import asyncio
from asgiref.sync import sync_to_async
from django.db.models import Q
from itertools import chain
from add.models import Comment, Saved, OfferedPrice, AddHistory, Add

# Create your views here.

class DashboardView(LoginRequiredMixin, View):

    async def get(self, request):
        adds = await sync_to_async(list)(Add.objects.filter(owner=request.user))
        comment_add_list = []
        saved_add_list = []
        offered_price_add_list = []
        add_history_add_list = []
        add_dict = {}
        for add in adds:    
            comments, saved, offered_price, add_history = await asyncio.gather(
                sync_to_async(Comment.objects.filter)(add=add),
                sync_to_async(Saved.objects.filter)(add=add),
                sync_to_async(OfferedPrice.objects.filter)(add=add),
                sync_to_async(AddHistory.objects.filter)(add=add)
            )
            add_dict[add] = {"comments":comments, "saved":saved, "offered_price":offered_price, "add_history":add_history}
            comment_add_list.append(comments)
            saved_add_list.append(saved)
            offered_price_add_list.append(offered_price)
            add_history_add_list.append(add_history)
        await self.helper_1(add_dict)
        contx = {"add_dict":add_dict}
        return await sync_to_async(render)(request, "dashboard/dashboard.html", contx)
    
    @sync_to_async
    def helper_1(self, add_dict):
        pint("helper1")
        for add, value in add_dict.items():
            pint(value)
            for i in add_dict[add]:
                pint(i)
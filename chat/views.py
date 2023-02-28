from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from .models import Group, ChatModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from home.models import UserUuid
from add.tests import pint
import asyncio
from asgiref.sync import sync_to_async
from django.http import HttpResponse, Http404
# Create your views here.


class ChatView(LoginRequiredMixin, View):
    
    def get(self, request, u_uuid):
        c_user = request.user # current user
        uuid_c = UserUuid.objects.get(user=c_user) # current user uuid
        uuid_o = UserUuid.objects.get(uuid=u_uuid) # other user uuid
        o_user = uuid_o.user # other user
        group_name, uu1, uu2 = self.sorting(uuid_c, uuid_o)
        if uu1 == uu2:
            raise Http404("you can't chat from yourself")
        group, t = Group.objects.get_or_create(group_name=group_name, user1=uu1, user2=uu2)
        chats = ChatModel.objects.filter(group=group)
        contx = {"group_name":group.group_name, "chats":chats, "other_user":o_user, 'user_uuid':str(uuid_c)}
        return render(request, "chat/chat.html", contx)
    
    def sorting(self, u1, u2):
        lis = [str(u1), str(u2)]
        lis.sort()
        uu1 = UserUuid.objects.get(uuid=lis[0]) # sorted user 1
        uu2 = UserUuid.objects.get(uuid=lis[1]) # sorted user 2
        group_name = ".".join(lis)
        return group_name, uu1.user, uu2.user

class ChatListView(LoginRequiredMixin, View):

    def get(self, request):
        groups = Group.objects.filter(user1=request.user) | Group.objects.filter(user2=request.user)
        pint(groups)
        contx = {'groups':groups}
        return render(request, 'chat/chat_list.html', contx)
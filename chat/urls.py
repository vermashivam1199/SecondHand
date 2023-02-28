from django.views.generic import TemplateView
from django.urls import path
from .views import ChatView, ChatListView

app_name = 'chat'
urlpatterns = [
    path('new_chat/<str:u_uuid>', ChatView.as_view(), name='chat_'),
    path('chat_list/', ChatListView.as_view(), name='chat_list'),
]
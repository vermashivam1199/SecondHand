from django.urls import path
from .views import NotificationListView, NotificationDetail


app_name = 'notification'
urlpatterns = [
    path('notification_list', NotificationListView.as_view(), name='notification_list'),
    path('notification_detail/<int:pk>/', NotificationDetail.as_view(), name='notification_deatil'),
]
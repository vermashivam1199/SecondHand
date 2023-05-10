from django.views.generic import TemplateView
from django.urls import path
from.views import (
    UserProfileView, OwnerProfilePhotoUpdateView, stream_profile_pic, OwnerProfilePhotoDeleteView, OwnerAboutView, CreateFavriouteView,
    DeleteFavriouteView, UserUpdateView, PasswordUpdateView, stream_profile_pic_chat, DashboardDetailView
)


app_name = 'user_profile'
urlpatterns = [
    path('', UserProfileView.as_view(), name='profile_page'),
    path('profile_photo/', OwnerProfilePhotoUpdateView.as_view(), name='profile_photo'),
    path('show_profile_photo/', stream_profile_pic, name='show_profile_photo'),
    path('profile_photo_delete/', OwnerProfilePhotoDeleteView.as_view(), name='profile_photo_delete'),
    path('owner_about/<int:pk>', OwnerAboutView.as_view(), name='owner_about'),
    path('create_favrioute/<int:pk>', CreateFavriouteView.as_view(), name='create_favrioute'),
    path('delete_favrioute/<int:pk>', DeleteFavriouteView.as_view(), name='delete_favrioute'),
    path('user_update/', UserUpdateView.as_view(), name='user_update'),
    path('password_update/', PasswordUpdateView.as_view(), name='password_update'),
    path('show_profile_photo_chat/<int:pk>', stream_profile_pic_chat, name='show_profile_photo_chat'),
    path('dashboard_deatil/<int:pk>', DashboardDetailView.as_view(), name='dashboard_deatil'),
]
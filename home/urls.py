from django.views.generic import TemplateView
from django.urls import path
from .views import RegisterView, HomeView


app_name = 'home'
urlpatterns = [
    path('homes', HomeView.as_view(), name='all'),
    path('register/', RegisterView.as_view(), name='register')
]
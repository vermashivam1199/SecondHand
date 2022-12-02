from django.views.generic import TemplateView
from django.urls import path
from.views import (
    AddListView, AddCreateView, PhotoCreateView, AddDetailView, AddUpdateView, stream_file, OwnerListView, OwnerDetailView, PhotoUpdateView, PhotoAddView,
    AddDeleteView, PhotoDeleteView, CommentView, CommentDeleteView, CreateSavedView, DeleteSavedView, OfferedPriceView, OfferedPriceDelete, FeatureView,
    FeatureUpdateView, FeatureDeleteView
)


app_name = 'add'
urlpatterns = [
    path('', AddListView.as_view(), name='add_list'),
    path('create/', AddCreateView.as_view(), name='add_create'),
    path('photo/', PhotoCreateView.as_view(), name='add_photo'),
    path('detail/<int:id>/', AddDetailView.as_view(), name='add_detail'),
    path('update/<int:id>/', AddUpdateView.as_view(), name='add_update'),
    path('pics/<int:id>/', stream_file, name='steam_pic'),
    path('owner_list/', OwnerListView.as_view(), name='owner_list'),
    path('owner_detail/<int:id>/', OwnerDetailView.as_view(), name='owner_detail'),
    path('picture_update/<int:pic_id>/<int:add_id>', PhotoUpdateView.as_view(), name='picture_update'),
    path('new_photo/<int:add_id>', PhotoAddView.as_view(), name='new_photo'),
    path('add_delete/<int:pk>', AddDeleteView.as_view(), name='add_delete'),
    path('photo_delete/<int:pk>', PhotoDeleteView.as_view(), name='photo_delete'),
    path('comment/<int:pk>', CommentView.as_view(), name='comment'),
    path('comment_delete/<int:pk>', CommentDeleteView.as_view(), name='comment_delete'),
    path('create_saved/<int:pk>', CreateSavedView.as_view(), name='create_saved'),
    path('delete_saved/<int:pk>', DeleteSavedView.as_view(), name='delete_saved'),
    path('offered_price/<int:pk>', OfferedPriceView.as_view(), name='offered_price'),
    path('offered_price_delete/<int:pk>', OfferedPriceDelete.as_view(), name='offered_price_delete'),
    path('feature_create/<int:pk>', FeatureView.as_view(), name='feature_create'),
    path('feature_update/<int:pk>', FeatureUpdateView.as_view(), name='feature_update'),
    path('feature_delete/<int:pk>', FeatureDeleteView.as_view(), name='feature_delete'),
]
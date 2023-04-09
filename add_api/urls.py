from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import AddAPI, PhotoAPI, CommentAPI, OfferedPriceAPI, FeatureAPI, CoverPhotoAPI, SavedAPI, FavriouteAPI


app_name = 'add_api'
router = DefaultRouter()
router.register(r'add', AddAPI, basename="add")
router.register(r'photo', PhotoAPI, basename="photo")
router.register(r'comment', CommentAPI, basename="comment")
router.register(r'offered_price', OfferedPriceAPI, basename="offered_price")
router.register(r'feature', FeatureAPI, basename="feature")
router.register(r'cover_photo', CoverPhotoAPI, basename="cover_photo")
router.register(r'saved', SavedAPI, basename="saved")
router.register(r'favrioute', FavriouteAPI, basename="favrioute")
# urlpatterns = router.urls

urlpatterns = [
    
    path("",include(router.urls))
   
]
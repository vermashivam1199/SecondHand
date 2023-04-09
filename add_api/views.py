from django.shortcuts import render
import django_filters.rest_framework
from add.tests import pint
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from .permissions import OwnerPermission, OwnerPermission2
from django.db.models import Q
from .serializers import (
    OfferedPriceSerializer, AddDetailSerializers, AddCreateSerializer, PhotoSerializer, CommentSerializer, FeatureSerializer, CoverPhotoSerializer, SavedSerializer, 
    FavriouteSerializer
)
from add.models import (
    Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo, Feature, CoverPhoto, Favrioute
)

# Create your views here.    

class BaseOwnerAPI(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset = self.model_class.objects.filter(owner=request.user)
        paginate_queryset = self.paginate_queryset(queryset)
        serializer = self.serializer_class(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        row = self.owner_serializer_class(data=request.data, context={"owner":str(request.user.id)})
        if row.is_valid():
            row.save()
            return Response(row.data, status=status.HTTP_201_CREATED)
        return Response(row.errors)

    
    def partial_update(self, request, pk, *args, **kwargs):
        saved = get_object_or_404(self.model_class, pk=pk)
        row = self.owner_serializer_class(saved, data=request.data, context={"owner":str(request.user.id)})
        if row.is_valid():
            row.save()
            return Response(row.data, status=status.HTTP_201_CREATED)
        return Response(row.errors)
    

    
class AddAPI(viewsets.ModelViewSet):
    queryset = Add.objects.all()
    serializer_class = AddCreateSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission]


    def list(self, request, *args, **kwargs):
        queryset = Add.objects.all()
        name = self.request.query_params.get('name')
        if name:
            name = name.replace("+"," ")
            queryset = Add.objects.filter(name=name)
        serializer_class_list = AddDetailSerializers
        serializer = AddDetailSerializers(queryset, many=True)
        paginate_queryset = self.paginate_queryset(queryset)
        serializer = serializer_class_list(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Add, pk=pk)
        serializer = AddDetailSerializers(obj)
        return Response(serializer.data)
    
class PhotoAPI(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission]

    def list(self, request, *args, **kwargs):
        return Response()
    
    def retrieve(self, request, pk, *args, **kwargs):
        return Response()
    

class CommentAPI(BaseOwnerAPI):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission2]
    owner_serializer_class = CommentSerializer
    model_class = Comment

    
class OfferedPriceAPI(BaseOwnerAPI):
    queryset = OfferedPrice.objects.all()
    serializer_class = OfferedPriceSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission]
    owner_serializer_class = OfferedPriceSerializer
    model_class = OfferedPrice


class FeatureAPI(BaseOwnerAPI):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission]
    owner_serializer_class = FeatureSerializer
    model_class = Feature

    def list(self, request, *args, **kwargs):
        queryset = self.model_class.objects.filter(Q(add__owner=request.user))
        serializer = AddDetailSerializers(queryset, many=True)
        paginate_queryset = self.paginate_queryset(queryset)
        serializer = self.serializer_class(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    
class CoverPhotoAPI(viewsets.ModelViewSet):
    queryset = CoverPhoto.objects.all()
    serializer_class = CoverPhotoSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission]

    def list(self, request, *args, **kwargs):
        return Response()
    
    def retrieve(self, request, pk, *args, **kwargs):
        return Response()
    
class SavedAPI(BaseOwnerAPI):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission2]
    owner_serializer_class = SavedSerializer
    model_class = Saved


class FavriouteAPI(BaseOwnerAPI):
    queryset = Favrioute.objects.all()
    serializer_class = FavriouteSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission2]
    owner_serializer_class = FavriouteSerializer
    model_class = Favrioute
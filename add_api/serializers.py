from rest_framework import serializers
from add.tests import pint
from django.contrib.auth.models import User
from add.models import (
    Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo, Feature, CoverPhoto, Favrioute
)


#serializers
class BaseOwnerValidation(serializers.ModelSerializer):
    def validate_owner(self, attrs):
        if self.context["owner"] == str(attrs.id):
            return attrs
        raise serializers.ValidationError("owner must be logined user")



class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]

class OfferedPriceSerializer(BaseOwnerValidation):
    class Meta:
        model = OfferedPrice
        fields = "__all__"

class CommentDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(many=False)
    class Meta:
        model = Comment
        fields = "__all__"
    
class CatagoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"

    def validate_add(self, attrs):
        if self.context["owner"] == str(attrs.id):
            pint(attrs.owner.id, "add validation", self.context["owner"])
            return attrs
        raise serializers.ValidationError("user must make feature of its own adds")
        
class PhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["content_type", "cover"]

class CoverPhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverPhoto
        fields = ["content_type", "add"]

class AddDetailSerializers(serializers.ModelSerializer):
    owner = OwnerSerializer(many=False, read_only=False)
    add_comment = CommentDetailSerializer(many=True, read_only=True)
    category = CatagoryDetailSerializer(many=False, read_only=False)
    add_feature = FeatureSerializer(many=True, read_only=True)
    add_photo = PhotoDetailSerializer(many=True, read_only=True)
    cover_photo = CoverPhotoDetailSerializer(many=False, read_only=True)
    class Meta:
        model = Add
        exclude = ["offered_price", "comment", "report", "saved", "counter"]

class AddCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add
        fields = ["id", "name", "description", "price", "category", "owner"]

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"

class CommentSerializer(BaseOwnerValidation):
    class Meta:
        model = Comment
        fields = "__all__"

class CoverPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverPhoto
        fields = "__all__"

class SavedSerializer(BaseOwnerValidation):
    class Meta:
        model = Saved
        fields = "__all__"

class FavriouteSerializer(BaseOwnerValidation):
    class Meta:
        model = Favrioute
        fields = "__all__"
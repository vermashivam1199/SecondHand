from rest_framework.permissions import BasePermission
from add.tests import pint


class OwnerPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user.is_authenticated:
                return super().has_permission(request, view)
            else:
                return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "DELETE", "PATCH"]:
            if request.user == obj.owner:
                return super().has_object_permission(request, view, obj)
            return False
        

class OwnerPermission2(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return super().has_permission(request, view)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in ["DELETE", "PATCH", "GET"]:
            if request.user == obj.owner:
                return super().has_object_permission(request, view, obj)
        elif request.method == "PUT":
            return False
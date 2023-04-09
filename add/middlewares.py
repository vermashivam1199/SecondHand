from .tests import pint
from django.shortcuts import HttpResponse
from .models import History, AddHistory, Add
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin

class MyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            row  = History(text=request.path, owner=request.user)
            row.save()
            if "add/detail" in request.path:
                add_pk = int(request.path[-2])
                add = get_object_or_404(Add, pk=add_pk)
                if request.user != add.owner:
                    add_history = AddHistory(add=add, owner=request.user)
                    add_history.save()


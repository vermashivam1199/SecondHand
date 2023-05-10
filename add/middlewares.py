from .tests import pint
from django.shortcuts import HttpResponse
from .models import History, AddHistory, Add
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin
import re

class MyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            row  = History(text=request.path, owner=request.user)
            row.save()
            pint("middleware working")
            if "add/detail/" in request.path:
                re_result = re.search(r"^/add/detail/(\d+?)/$", request.path)
                add_id = int(re_result.groups()[0])
                add = get_object_or_404(Add, pk=add_id)
                if request.user != add.owner:
                    add_history = AddHistory(add=add, owner=request.user)
                    add_history.save()
                    pint(add_history, "add history saved")


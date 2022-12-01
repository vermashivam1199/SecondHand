from multiprocessing import get_context
from django.views.generic import UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo)
from .tests import pint


class OwnerUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)



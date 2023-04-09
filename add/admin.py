from django.contrib import admin
from .models import (Add, Comment, Report, ReportCategory, History, Saved, Category, OfferedPrice, Photo, Favrioute, Feature, CoverPhoto, AddHistory)

# Register your models here.
@admin.register(Add)
class AddAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'description', 'price', 'category', 'owner'
    ]

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(ReportCategory)
admin.site.register(History)
admin.site.register(Saved)
admin.site.register(Photo)
admin.site.register(OfferedPrice)
admin.site.register(Favrioute)
admin.site.register(Feature)
admin.site.register(CoverPhoto)
admin.site.register(AddHistory)
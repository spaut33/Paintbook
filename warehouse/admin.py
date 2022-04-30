from django.contrib import admin

from .models import Manufacturer, Series, Paint, UserPaint


# Register your models here.
@admin.register(Paint)
class PaintAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    pass


@admin.register(UserPaint)
class UserPaintAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

from .models import Manufacturer, Series, Paint


# Register your models here.
class PaintAdmin(admin.ModelAdmin):
    pass


admin.site.register(Paint, PaintAdmin)
admin.site.register(Manufacturer)
admin.site.register(Series)

from django.contrib import admin

from .models import Manufacturer, Serie, Paint


# Register your models here.
class PaintAdmin(admin.ModelAdmin):
    pass


admin.site.register(Paint, PaintAdmin)
admin.site.register(Manufacturer)
admin.site.register(Serie)

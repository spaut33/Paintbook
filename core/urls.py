"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from warehouse.views import PaintsViewSet, UserPaintViewSet, auth

router = SimpleRouter()

router.register('paints', PaintsViewSet)
router.register('user_paints', UserPaintViewSet)

# admin, social auth routes
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('__reload__/', include('django_browser_reload.urls')),
    path('auth/', auth),
]

# API endpoint
urlpatterns = [
    path(
        'api/v1/', include((router.urls, 'warehouse'), namespace='warehouse')
    ),
] + urlpatterns

urlpatterns = [
    # ...
    path('__debug__/', include('debug_toolbar.urls')),
] + urlpatterns

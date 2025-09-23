"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('importer/', include('importer.urls')),
]

# API-only root endpoint
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Australian Visa Data API',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'filter_options': '/api/filter-options/',
            'visa_data': '/api/visa-data/'
        },
        'frontend': 'https://ausvisa.vercel.app',
        'status': 'healthy'
    })

urlpatterns += [
    path('', api_root, name='api_root'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

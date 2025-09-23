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

# Serve React app
if not settings.DEBUG:
    # In production, serve the React build
    urlpatterns += [
        path('', TemplateView.as_view(template_name='index.html'), name='home'),
    ]
else:
    # In development, show a simple message
    from django.http import HttpResponse
    from django.urls import path

    def home_view(request):
        return HttpResponse("""
        <h1>Django API Server</h1>
        <p>API is running at <a href="/api/">/api/</a></p>
        <p>Admin panel at <a href="/admin/">/admin/</a></p>
        <p>React frontend should be served separately in development</p>
        """)

    urlpatterns += [
        path('', home_view, name='home'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

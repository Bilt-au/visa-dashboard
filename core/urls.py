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
from django.views.generic import RedirectView
from django.http import HttpResponse
import os

def serve_react_app(request):
    static_root = settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'staticfiles')
    index_path = os.path.join(static_root, 'index.html')

    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    else:
        return HttpResponse("""
        <h1>Django API Server</h1>
        <p>API is running at <a href="/api/">/api/</a></p>
        <p>Admin panel at <a href="/admin/">/admin/</a></p>
        <p>React frontend not found</p>
        """)

urlpatterns += [
    path('', serve_react_app, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

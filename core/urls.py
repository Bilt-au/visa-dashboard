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
    # Try multiple possible locations for index.html
    possible_paths = [
        os.path.join(settings.BASE_DIR, 'staticfiles', 'index.html'),
        os.path.join(settings.BASE_DIR, 'static', 'index.html'),
    ]

    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        possible_paths.insert(0, os.path.join(settings.STATIC_ROOT, 'index.html'))

    for index_path in possible_paths:
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                return HttpResponse(f.read(), content_type='text/html')

    # Debug info
    debug_info = f"""
    <h1>Django API Server</h1>
    <p>API is running at <a href="/api/">/api/</a></p>
    <p>Admin panel at <a href="/admin/">/admin/</a></p>
    <p>React frontend not found</p>
    <br>
    <h3>Debug Info:</h3>
    <p>BASE_DIR: {settings.BASE_DIR}</p>
    <p>STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', 'Not set')}</p>
    <p>Checked paths:</p>
    <ul>
    """
    for path in possible_paths:
        exists = "✓" if os.path.exists(path) else "✗"
        debug_info += f"<li>{exists} {path}</li>"
    debug_info += "</ul>"

    return HttpResponse(debug_info)

urlpatterns += [
    path('', serve_react_app, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

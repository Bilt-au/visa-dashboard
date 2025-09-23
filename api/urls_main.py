from django.urls import path, include

urlpatterns = [
    path('data/', include('api.urls.data')),
]
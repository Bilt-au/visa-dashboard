from django.urls import path
from .. import views

urlpatterns = [
    path('visa-data/', views.get_visa_data, name='get_visa_data'),
    path('filter-options/', views.get_filter_options, name='get_filter_options'),
]
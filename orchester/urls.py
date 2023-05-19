from django.urls import path
from . import views

urlpatterns = [
    path('/payment-upgrade', views.service_orchester),
    path('/payment-upgrade-convert', views.service_orchester_convert)
]
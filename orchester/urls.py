from django.urls import path
from . import views

urlpatterns = [
    path('api/payment/create-payment', views.payment_service),
    path('api/convert/pdf-to-img', views.convert_service),
    path('', views.service_orchester),
]
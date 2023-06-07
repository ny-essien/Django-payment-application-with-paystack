from django.urls import path
from . import views

urlpatterns = [

    path('', views.initiate_payments, name = 'initiate_payments'),

    path('<str:ref>/', views.verify_payment, name = "verify_payment"),
]
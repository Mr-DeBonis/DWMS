from django.urls import path

from SAIApp import views


app_name = "SAIApp"

urlpatterns = [
    path('', views.index, name='index'),
    path('DWMSDespacho/', views.DWMSDespacho, name='DWMSDespacho'),
    path('DWMSRecepcion/', views.DWMSRecepcion, name='DWMSRecepcion'),

]
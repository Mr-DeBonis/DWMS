from django.urls import path

from SAIApp import views


app_name = "SAIApp"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('DWMSDespacho/', views.DWMSDespacho, name='DWMSDespacho'),
    path('DWMSDespachoIngresar/', views.DWMSDespachoIngresar, name='DWMSDespachoIngresar'),
    path('DWMSDespachoDetalle/<despacho_id>', views.DWMSDespachoDetalle, name='DWMSDespachoDetalle'),
    path('DWMSDespachoAgregarGuia/<despacho_id>', views.DWMSDespachoAgregarGuia, name='DWMSDespachoAgregarGuia'),
    path('DWMSRecepcion/', views.DWMSRecepcion, name='DWMSRecepcion'),

]
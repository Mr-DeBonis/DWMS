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
    path('DWMSDespachoVerGuia/<guia_desp_id>', views.DWMSDespachoVerGuia, name='DWMSDespachoVerGuia'),
    path('DWMSDespachoEditarGuia/<guia_desp_id>', views.DWMSDespachoEditarGuia, name='DWMSDespachoEditarGuia'),
    path('DWMSDespachoEliminarFotoGuia/<foto_id>', views.DWMSDespachoEliminarFotoGuia, name='DWMSDespachoEliminarFotoGuia'),
    path('DWMSRecepcion/', views.DWMSRecepcion, name='DWMSRecepcion'),

]
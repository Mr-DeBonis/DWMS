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
    path('DWMSDespachoEditar/<despacho_id>', views.DWMSDespachoEditar, name='DWMSDespachoEditar'),
    path('DWMSDespachoEliminar/<despacho_id>', views.DWMSDespachoEliminar, name='DWMSDespachoEliminar'),
    path('DWMSDespachoAgregarGuia/<despacho_id>', views.DWMSDespachoAgregarGuia, name='DWMSDespachoAgregarGuia'),
    path('DWMSDespachoVerGuia/<guia_desp_id>', views.DWMSDespachoVerGuia, name='DWMSDespachoVerGuia'),
    path('DWMSDespachoEditarGuia/<guia_desp_id>', views.DWMSDespachoEditarGuia, name='DWMSDespachoEditarGuia'),
    path('DWMSDespachoEliminarGuia/<guia_desp_id>', views.DWMSDespachoEliminarGuia, name='DWMSDespachoEliminarGuia'),
    path('DWMSDespachoEliminarFotoGuia/<foto_id>', views.DWMSDespachoEliminarFotoGuia, name='DWMSDespachoEliminarFotoGuia'),
    path('DWMSDespachoEliminarFoto/<foto_id>', views.DWMSDespachoEliminarFoto, name='DWMSDespachoEliminarFoto'),
    path('DWMSRecepcion/', views.DWMSRecepcion, name='DWMSRecepcion'),
    path('DWMSRecepcionIngresar/', views.DWMSRecepcionIngresar, name='DWMSRecepcionIngresar'),
    path('DWMSRecepcionDetalle/<recepcion_id>', views.DWMSRecepcionDetalle, name='DWMSRecepcionDetalle'),
    path('DWMSRecepcionEditar/<recepcion_id>', views.DWMSRecepcionEditar, name='DWMSRecepcionEditar'),
    path('DWMSRecepcionEliminar/<recepcion_id>', views.DWMSRecepcionEliminar, name='DWMSRecepcionEliminar'),
    path('DWMSRecepcionAgregarGuia/<recepcion_id>', views.DWMSRecepcionAgregarGuia, name='DWMSRecepcionAgregarGuia'),
    path('DWMSRecepcionVerGuia/<guia_rec_id>', views.DWMSRecepcionVerGuia, name='DWMSRecepcionVerGuia'),
    path('DWMSRecepcionEditarGuia/<guia_rec_id>', views.DWMSRecepcionEditarGuia, name='DWMSRecepcionEditarGuia'),
    path('DWMSRecepcionEliminarGuia/<guia_rec_id>', views.DWMSRecepcionEliminarGuia, name='DWMSRecepcionEliminarGuia'),
    path('DWMSRecepcionEliminarFotoGuia/<foto_id>', views.DWMSRecepcionEliminarFotoGuia, name='DWMSRecepcionEliminarFotoGuia'),
    path('DWMSRecepcionEliminarFoto/<foto_id>', views.DWMSRecepcionEliminarFoto, name='DWMSRecepcionEliminarFoto'),
]
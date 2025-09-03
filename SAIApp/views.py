from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return redirect("SAIApp:DWMSDespacho")


def DWMSDespacho(request):
    return render(request, 'SAIApp/DWMSDespacho.html')


def DWMSRecepcion(request):
    return render(request, 'SAIApp/DWMSRecepcion.html')

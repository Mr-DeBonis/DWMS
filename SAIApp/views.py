from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    if request.user is None:
        return redirect('SAIApp:login')
    else:
        return redirect("SAIApp:DWMSDespacho")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Ha ingresado a DWMS')
            return redirect('SAIApp:index')
        else:
            messages.success(request, 'Ha habido un error. Intente nuevamente.')
            return redirect('SAIApp:login')
    else:
        return render(request, 'SAIApp/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Ha salido de la plataforma")
    return redirect('SAIApp:index')


def DWMSDespacho(request):
    return render(request, 'SAIApp/DWMSDespacho.html')


def DWMSRecepcion(request):
    return render(request, 'SAIApp/DWMSRecepcion.html')

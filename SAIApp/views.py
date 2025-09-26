from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from SAIApp.forms import FormGuiaHeader, FormDespacho, FormGuiaDespachada
from SAIApp.models import dwms_despacho, dwms_foto_despacho, dwms_foto_guia_desp, dwms_guia_desp


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
    despachos = []
    if request.method == "POST":
        form = FormGuiaHeader(request.POST)
        if form.is_valid():
            folio = form.cleaned_data['folio']
            despachos = dwms_despacho.objects.filter(dwms_guia_desp__guia_header__folio=folio).order_by('-fecha_despacho')
            if len(despachos) == 0:
                messages.warning(request, "No se han encontrado despachos asociados")
    else:
        form = FormGuiaHeader()
        despachos = dwms_despacho.objects.all().order_by('-fecha_despacho')


    context = {
        'form': form,
        'despachos': despachos
    }
    return render(request, 'SAIApp/DWMSDespacho.html', context=context)


def DWMSDespachoIngresar(request):
    if request.method == 'POST':
        form = FormDespacho(request.POST)
        files = request.FILES.getlist('filepond')
        if form.is_valid():
            despacho = form.save(commit=False)
            despacho.current_user = request.user
            despacho.save()

            for file in files:
                dwms_foto_despacho.objects.create(
                    despacho=despacho,
                    foto=file
                )

            messages.success(request, "Despacho guardado")
            print("Success, saved as " + str(despacho.pk))

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'despacho_id': despacho.pk})

            return redirect('SAIApp:DWMSDespachoDetalle', despacho_id=despacho.pk)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = FormDespacho()

    context = {
        'form': form,
    }
    return render(request, 'SAIApp/DWMSDespachoIngresar.html', context=context)


def DWMSDespachoDetalle(request, despacho_id):
    despacho = dwms_despacho.objects.get(pk=despacho_id)
    fotos = dwms_foto_despacho.objects.filter(despacho=despacho)
    guias = dwms_guia_desp.objects.filter(despacho=despacho)

    context = {
        'despacho': despacho,
        'fotos': fotos,
        'guias': guias,
    }
    return render(request, 'SAIApp/DWMSDespachoDetalle.html', context=context)


def DWMSDespachoAgregarGuia(request, despacho_id):
    despacho = dwms_despacho.objects.get(pk=despacho_id)

    if request.method == 'POST':
        form = FormGuiaDespachada(request.POST)
        files = request.FILES.getlist('filepond')
        if form.is_valid():
            dwms_guia_desp = form.save(commit=False)
            dwms_guia_desp.current_user = request.user
            dwms_guia_desp.save()

            for file in files:
                dwms_foto_guia_desp.objects.create(
                    guia_desp=dwms_guia_desp,
                    foto=file
                )

            messages.success(request, "Guía guardada")
            print("Success, saved as " + str(dwms_guia_desp.pk))

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'despacho_id': despacho.pk})

            return redirect('SAIApp:DWMSDespachoDetalle', despacho_id=despacho.pk)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)

    else:
        form = FormGuiaDespachada(initial={'despacho': despacho})

    context = {
        'despacho': despacho,
        'form': form,
    }
    return render(request, 'SAIApp/DWMSDespachoAgregarGuia.html', context=context)


def DWMSRecepcion(request):
    return render(request, 'SAIApp/DWMSRecepcion.html')

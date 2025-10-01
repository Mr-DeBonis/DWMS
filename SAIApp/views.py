from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from SAIApp.forms import FormGuiaHeader, FormDespacho, FormGuiaDespachada, FormGuiaHeaderRecibida, FormRecepcion
from SAIApp.models import dwms_despacho, dwms_foto_despacho, dwms_foto_guia_desp, dwms_guia_desp, dwms_recepcion, \
    dwms_foto_recepcion, dwms_guia_recibida, dwms_foto_guia_recibida


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


def DWMSDespachoEditar(request, despacho_id):
    despacho = dwms_despacho.objects.get(pk=despacho_id)
    fotos = dwms_foto_despacho.objects.filter(despacho=despacho)

    if request.method == 'POST':
        form = FormDespacho(request.POST, instance=despacho)
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

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'despacho_id': despacho.pk})

            return redirect('SAIApp:DWMSDespachoDetalle', despacho_id=despacho.pk)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = FormDespacho(instance=despacho)

    context = {
        'despacho': despacho,
        'form': form,
        'fotos': fotos,
    }
    return render(request, 'SAIApp/DWMSDespachoEditar.html', context=context)


def DWMSDespachoEliminar(request, despacho_id):
    try:
        despacho = dwms_despacho.objects.get(pk=despacho_id)
        print("Borrando despacho " + str(despacho.pk))
        despacho.delete()
        messages.success(request, "El despacho ha sido borrado")
    except dwms_despacho.DoesNotExist:
        messages.error(request, "Este despacho no existe")
    finally:
        return redirect('SAIApp:DWMSDespacho')

def DWMSDespachoEliminarFoto(request, foto_id):
    if request.method == 'POST':
        try:
            foto = dwms_foto_despacho.objects.get(pk=foto_id)
            despacho = foto.despacho
            despacho.current_user = request.user
            despacho.save()
            foto.delete()
            return JsonResponse({"success": True})
        except dwms_foto_guia_desp.DoesNotExist:
            pass
    return JsonResponse({"error": "Petición inválida"}, status=400)


def DWMSDespachoAgregarGuia(request, despacho_id):
    despacho = dwms_despacho.objects.get(pk=despacho_id)

    if request.method == 'POST':
        form = FormGuiaDespachada(request.POST)
        files = request.FILES.getlist('filepond')

        if form.is_valid():
            guia_header = form.guia_header
            if dwms_guia_desp.objects.filter(guia_header=guia_header).exists():
                form.add_error('folio', "El folio " + str(guia_header.folio) + " ya está asignado a un despacho.")
                return JsonResponse({'errors': form.errors}, status=400)
            guia_desp = form.save(commit=False)
            guia_desp.current_user = request.user
            guia_desp.save()

            for file in files:
                dwms_foto_guia_desp.objects.create(
                    guia_desp=guia_desp,
                    foto=file
                )

            messages.success(request, "Guía guardada")
            print("Success, saved as " + str(guia_desp.pk))

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


def DWMSDespachoVerGuia(request, guia_desp_id):
    guia_desp = dwms_guia_desp.objects.get(pk=guia_desp_id)
    fotos = dwms_foto_guia_desp.objects.filter(guia_desp=guia_desp)
    context = {
        'guia_desp': guia_desp,
        'fotos': fotos,
    }
    return render(request, 'SAIApp/DWMSDespachoVerGuia.html', context=context)


def DWMSDespachoEditarGuia(request, guia_desp_id):
    guia_desp = dwms_guia_desp.objects.get(pk=guia_desp_id)
    fotos = dwms_foto_guia_desp.objects.filter(guia_desp=guia_desp)

    if request.method == 'POST':
        form = FormGuiaDespachada(request.POST, instance=guia_desp)
        files = request.FILES.getlist('filepond')

        if form.is_valid():
            guia_header = form.guia_header

            if dwms_guia_desp.objects.filter(guia_header=guia_header).exclude(despacho=guia_desp.despacho).exists():
                form.add_error('folio', "El folio " + str(guia_header.folio) + " ya está asignado a otro despacho.")
                return JsonResponse({'errors': form.errors}, status=400)

            guia_desp = form.save(commit=False)
            guia_desp.current_user = request.user
            guia_desp.save()

            for file in files:
                dwms_foto_guia_desp.objects.create(
                    guia_desp=guia_desp,
                    foto=file
                )

            messages.success(request, "Guía guardada")
            print("Success, saved as " + str(guia_desp.pk))

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'despacho_id': guia_desp.despacho.pk})

            return redirect('SAIApp:DWMSDespachoDetalle', despacho_id=guia_desp.despacho.pk)

        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = FormGuiaDespachada(instance=guia_desp)

    context = {
        'guia_desp': guia_desp,
        'fotos': fotos,
        'form': form,
    }
    return render(request, 'SAIApp/DWMSDespachoEditarGuia.html', context=context)


def DWMSDespachoEliminarGuia(request, guia_desp_id):
    try:
        guia_desp = dwms_guia_desp.objects.get(pk=guia_desp_id)
        print("Borrando guia " + str(guia_desp.pk))
        guia_desp.delete()
        messages.success(request, "La guía folio " + str(guia_desp.guia_header.folio) + " ha sido borrada")
        return redirect('SAIApp:DWMSDespachoDetalle', guia_desp.despacho.pk)
    except dwms_guia_desp.DoesNotExist:
        messages.error(request, "Esta guía no existe")
        return redirect('SAIApp:DWMSDespacho')


def DWMSDespachoEliminarFotoGuia(request, foto_id):
    if request.method == 'POST':
        try:
            foto = dwms_foto_guia_desp.objects.get(pk=foto_id)
            guia_desp = foto.guia_desp
            guia_desp.current_user = request.user
            guia_desp.save()
            foto.delete()
            return JsonResponse({"success": True})
        except dwms_foto_guia_desp.DoesNotExist:
            pass
    return JsonResponse({"error": "Petición inválida"}, status=400)


def DWMSRecepcion(request):
    recepciones = []
    if request.method == "POST":
        form = FormGuiaHeaderRecibida(request.POST)
        if form.is_valid():
            folio = form.cleaned_data['folio']
            recepciones = dwms_recepcion.objects.filter(dwms_guia_recibida__folio=folio).order_by('-fecha_recepcion')
            if len(recepciones) == 0:
                messages.warning(request, "No se han encontrado recepciones asociadas")
    else:
        form = FormGuiaHeaderRecibida()
        recepciones = dwms_recepcion.objects.all().order_by('-fecha_recepcion')

    context = {
        'form': form,
        'recepciones': recepciones
    }
    return render(request, 'SAIApp/DWMSRecepcion.html', context=context)


def DWMSRecepcionIngresar(request):
    if request.method == 'POST':
        form = FormRecepcion(request.POST)
        files = request.FILES.getlist('filepond')
        if form.is_valid():
            recepcion = form.save(commit=False)
            recepcion.current_user = request.user
            recepcion.save()

            for file in files:
                dwms_foto_recepcion.objects.create(
                    recepcion=recepcion,
                    foto=file
                )

            messages.success(request, "Recepción guardada")
            print("Success, saved as " + str(recepcion.pk))

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'recepcion_id': recepcion.pk})

            return redirect('SAIApp:DWMSRecepcionDetalle', recepcion_id=recepcion.pk)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = FormRecepcion()

    context = {
        'form': form,
    }
    return render(request, 'SAIApp/DWMSRecepcionIngresar.html', context=context)


def DWMSRecepcionDetalle(request, recepcion_id):
    recepcion = dwms_recepcion.objects.get(pk=recepcion_id)
    fotos = dwms_foto_recepcion.objects.filter(recepcion=recepcion)
    guias = dwms_guia_recibida.objects.filter(recepcion=recepcion)

    context = {
        'recepcion': recepcion,
        'fotos': fotos,
        'guias': guias,
    }
    return render(request, 'SAIApp/DWMSRecepcionDetalle.html', context=context)


def DWMSRecepcionEditar(request, recepcion_id):
    recepcion = dwms_recepcion.objects.get(pk=recepcion_id)
    fotos = dwms_foto_recepcion.objects.filter(recepcion=recepcion)

    if request.method == 'POST':
        form = FormRecepcion(request.POST, instance=recepcion)
        files = request.FILES.getlist('filepond')

        if form.is_valid():
            recepcion = form.save(commit=False)
            recepcion.current_user = request.user
            recepcion.save()

            for file in files:
                dwms_foto_recepcion.objects.create(
                    recepcion=recepcion,
                    foto=file
                )

            messages.success(request, "Recepción guardada")

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'recepcion_id': recepcion.pk})

            return redirect('SAIApp:DWMSRecepcionDetalle', recepcion_id=recepcion.pk)
        else:
            print(form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = FormRecepcion(instance=recepcion)

    context = {
        'recepcion': recepcion,
        'form': form,
        'fotos': fotos,
    }
    return render(request, 'SAIApp/DWMSRecepcionEditar.html', context=context)


def DWMSRecepcionEliminar(request, recepcion_id):
    try:
        recepcion = dwms_recepcion.objects.get(pk=recepcion_id)
        print("Borrando recepcion " + str(recepcion.pk))
        recepcion.delete()
        messages.success(request, "La recepción ha sido borrada")
    except dwms_recepcion.DoesNotExist:
        messages.error(request, "Esta recepción no existe")
    finally:
        return redirect('SAIApp:DWMSRecepcion')


def DWMSRecepcionAgregarGuia(request, recepcion_id):
    pass


def DWMSRecepcionVerGuia(request, guia_rec_id):
    pass


def DWMSRecepcionEditarGuia(request, guia_rec_id):
    pass


def DWMSRecepcionEliminarGuia(request, guia_rec_id):
    pass


def DWMSRecepcionEliminarFotoGuia(request, foto_id):
    pass


def DWMSRecepcionEliminarFoto(request, foto_id):
    if request.method == 'POST':
        try:
            foto = dwms_foto_recepcion.objects.get(pk=foto_id)
            recepcion = foto.recepcion
            recepcion.current_user = request.user
            recepcion.save()
            foto.delete()
            return JsonResponse({"success": True})
        except dwms_foto_recepcion.DoesNotExist:
            return JsonResponse({"error": "Esta foto no existe"})
    return JsonResponse({"error": "Petición inválida"}, status=400)

import os
import time
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone


class dwms_guia_header(models.Model):
    folio = models.IntegerField(blank=True, null=True, verbose_name='Folio')

    class Meta:
        verbose_name = 'Guia'
        verbose_name_plural = 'Guias'

## Guias Pickeadas
class dwms_g_pickeada(models.Model):
    header = models.ForeignKey('dwms_guia_header', on_delete=models.PROTECT)
    fecha  = models.DateTimeField(default=datetime.now, blank=True)
    user   = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Guia Pickeada'
        verbose_name_plural = 'Guias Pickeada'

## Guias control salida
class dwms_g_c_salida(models.Model):
    header = models.ForeignKey('dwms_guia_header',on_delete=models.PROTECT)
    fecha  = models.DateTimeField(default=datetime.now, blank=True)
    user   = models.ForeignKey(User, verbose_name='Usuario',on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Guia Control Salida'
        verbose_name_plural = 'Guias Control Salida'

# Transporte
class dwms_transporte(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'

    def __str__(self):
        return self.nombre


# Despachos
class dwms_despacho(models.Model):
    nota = models.CharField(max_length=255, blank=True, verbose_name="Notas")
    transporte = models.ForeignKey(dwms_transporte, verbose_name='Transporte', on_delete=models.PROTECT)
    otro_transporte = models.CharField(max_length=255, blank=True, null=True, verbose_name='Otro Transporte')
    fecha_despacho = models.DateTimeField(default=datetime.now, verbose_name='Fecha de Despacho')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    creacion_user = models.ForeignKey(User, verbose_name='Usuario de Creación', on_delete=models.PROTECT)
    mod_user = models.ForeignKey(User, related_name='mod_user_despacho', verbose_name='Usuario de Modificación', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'

    def save(self, *args, **kwargs):
        # If current_user has been set externally (from the view)
        user = getattr(self, 'current_user', None)

        if not self.pk:
            # new object
            if user is not None:
                self.creacion_user = user
                self.mod_user = user
                self.fecha_creacion = timezone.now()
        else:
            # updating existing object
            if user is not None:
                self.mod_user = user
        self.fecha_modificacion = timezone.now()

        super().save(*args, **kwargs)


def dwms_foto_despacho_path(instance, filename):
    name, ext = os.path.splitext(filename)
    if not ext:
        ext = '.jpg'
    return 'DWMS_Despacho/{0}_{1}{2}'.format(instance.despacho.id, int(time.time()*1000.0), ext)


class dwms_foto_despacho(models.Model):
    despacho = models.ForeignKey(dwms_despacho, on_delete=models.PROTECT)
    foto = models.ImageField(upload_to=dwms_foto_despacho_path)
    filename = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        verbose_name = "Foto despacho"
        verbose_name_plural = "Fotos despacho"


@receiver(pre_delete, sender=dwms_foto_despacho)
def dwms_foto_despacho_delete(sender, instance, **kwargs):
    instance.foto.delete(False)


class dwms_guia_desp(models.Model):
    guia_header = models.ForeignKey(dwms_guia_header, on_delete=models.PROTECT)
    despacho = models.ForeignKey(dwms_despacho, on_delete=models.PROTECT)
    ot_transporte = models.CharField(max_length=50, blank=True, null=True, verbose_name='Orden de Transporte')
    nota = models.CharField(max_length=255, blank=True, verbose_name="Notas")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    creacion_user = models.ForeignKey(User, verbose_name='Usuario de Creación', on_delete=models.PROTECT)
    mod_user = models.ForeignKey(User, related_name='mod_user_guia_desp', verbose_name='Usuario de Modificación', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Guia despachada'
        verbose_name_plural = 'Guias despachadas'


def dwms_foto_guia_desp_path(instance, filename):
    name, ext = os.path.splitext(filename)
    if not ext:
        ext = '.jpg'
    return 'DWMS_Guia_Desp/{0}_{1}{2}'.format(instance.guia_desp.id, int(time.time()*1000.0), ext)


class dwms_foto_guia_desp(models.Model):
    guia_desp = models.ForeignKey(dwms_guia_desp, on_delete=models.PROTECT)
    foto = models.ImageField(upload_to=dwms_foto_guia_desp_path)
    filename = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        verbose_name = "Foto guia despachada"
        verbose_name_plural = "Fotos guias despachadas"


@receiver(pre_delete, sender=dwms_foto_guia_desp)
def dwms_foto_guia_desp_delete(sender, instance, **kwargs):
    instance.foto.delete(False)


# Proveedores
class dwms_proveedor(models.Model):
    rut = models.CharField(max_length=30, blank=True, null=True, verbose_name='RUT')
    razon_social = models.CharField(max_length=320, blank=True, null=True, verbose_name='Cliente')

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.razon_social


# Recepciones
class dwms_recepcion(models.Model):
    nota = models.CharField(max_length=255, blank=True, verbose_name="Notas")
    transporte = models.ForeignKey(dwms_transporte, verbose_name='Transporte', on_delete=models.PROTECT)
    otro_transporte = models.CharField(max_length=255, blank=True,null=True, verbose_name='Otro Transporte')
    fecha_recepcion = models.DateTimeField(default=datetime.now, verbose_name='Fecha de recepción')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    creacion_user = models.ForeignKey(User, verbose_name='Usuario de Creación', on_delete=models.PROTECT)
    mod_user = models.ForeignKey(User, related_name='mod_user_recepcion', verbose_name='Usuario de Modificación', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'


def dwms_foto_recepcion_path(instance, filename):
    name, ext = os.path.splitext(filename)
    if not ext:
        ext = '.jpg'
    return 'DWMS_Recepcion/{0}_{1}{2}'.format(instance.recepcion.id, int(time.time()*1000.0), ext)


class dwms_foto_recepcion(models.Model):
    recepcion = models.ForeignKey(dwms_recepcion, on_delete=models.PROTECT)
    foto = models.ImageField(upload_to=dwms_foto_recepcion_path)
    filename = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        verbose_name = "Foto recepción"
        verbose_name_plural = "Fotos recepción"


@receiver(pre_delete, sender=dwms_foto_recepcion)
def dwms_foto_recepcion_delete(sender, instance, **kwargs):
    instance.foto.delete(False)


class dwms_guia_recibida(models.Model):
    recepcion = models.ForeignKey(dwms_recepcion, on_delete=models.PROTECT)
    ot_transporte = models.CharField(max_length=50, blank=True, null=True, verbose_name='Orden de Transporte')
    nota = models.CharField(max_length=255, blank=True, verbose_name="Notas")
    cantidad_bultos = models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Bultos')
    folio = models.IntegerField(blank=True, null=True, verbose_name='Folio')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    creacion_user = models.ForeignKey(User, verbose_name='Usuario de Creación', on_delete=models.PROTECT)
    mod_user = models.ForeignKey(User, related_name='mod_user_guia_recibida', verbose_name='Usuario de Modificación', on_delete=models.PROTECT)
    proveedor = models.ForeignKey(dwms_proveedor, verbose_name='Proveedor', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Guia recibida'
        verbose_name_plural = 'Guias recibidas'


def dwms_foto_guia_recibida_path(instance, filename):
    name, ext = os.path.splitext(filename)
    if not ext:
        ext = '.jpg'
    return 'DWMS_Guia_Recibida/{0}_{1}{2}'.format(instance.guia_recibida.id, int(time.time()*1000.0), ext)


class dwms_foto_guia_recibida(models.Model):
    guia_recibida = models.ForeignKey(dwms_guia_recibida, on_delete=models.PROTECT)
    foto = models.ImageField(upload_to=dwms_foto_guia_recibida_path)
    filename = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        verbose_name = "Foto guia recibida"
        verbose_name_plural = "Fotos guias recibidas"


@receiver(pre_delete, sender=dwms_foto_guia_recibida)
def dwms_foto_guia_recibida_delete(sender, instance, **kwargs):
    instance.foto.delete(False)



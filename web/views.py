from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from web.formularios import *
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.forms import formset_factory,modelformset_factory
from django.views.generic import View
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import OrdenTrabajo


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def handler403(request,exception):
    return render(request, '403.html',status=403)

class index(TemplateView):
  template_name = "index.html"


class login(TemplateView):
  template_name = "login.html"

class dashboard(TemplateView):
  template_name = "dashboard.html"


class clienteCrearView(CreateView):
  template_name= "registro-cliente.html"
  model = Cliente
  form_class = ClienteForm


class cotizacionCrearView(TemplateView):
  template_name= "crear-cotizacion.html"
  form_class = CotizacionForm

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["form"] = self.form_class()
      context["form"].fields["cotizado_por"].initial = self.request.user.empleado
      context["form2"] = ClienteOrdenForm()
      context["formset"] = formset_factory(ServiciosForm, extra=1)
      return context

  def post(self, request, *args, **kwargs):
    cotizacion = self.form_class(request.POST)
    cliente = ClienteOrdenForm(request.POST)
    formset = formset_factory(ServiciosForm)(request.POST)

    if cotizacion.is_valid() and cliente.is_valid() and formset.is_valid():
      data = cliente.cleaned_data
      if data["clientes"]:
        cl = data["clientes"]
      else:
        cl = cliente.save()

      cot = cotizacion.save(commit=False)
      cot.cliente = cl
      cot.save()

      for servicio in formset.forms:
        ser = servicio.save(commit=False)
        ser.cotizacion = cot
        ser.save()
    else:
      context = self.get_context_data()
      context["form"] = cotizacion
      context["form2"] = cliente
      context["formset"] = formset

      return render(request, self.template_name, context)

    return redirect(reverse_lazy("cotizaciones-lista"))


class userCrearView(CreateView):
  template_name= "registro-cliente.html"
  model = User
  form_class = EmpleadoForm
  success_url = "empleados-lista"
  title = "registro de usuario"

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = self.title
      return context

class cotizacionListView(ListView):
  paginate_by = 10
  template_name = "cotizaciones-lista.html"
  model = Cotizacion
  queryset = Cotizacion.objects.filter(activo=True)

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['btn_url'] = reverse_lazy('cotizaciones-d-lista')
    context['btn_act'] = "Ver cotizaciones borradas"

    return context

class cotizacionDeactivateListView(ListView):
  paginate_by = 10
  template_name = "cotizaciones-lista.html"
  model = Cotizacion
  queryset = Cotizacion.objects.filter(activo=False)

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['btn_url'] = reverse_lazy('cotizaciones-lista')
    context['btn_act'] = "Ver cotizaciones"
    context['deleted'] = True
    context['del_text'] = 'borradas'
    return context

class cotizacionDeactivateView(TemplateView):
  template_name = ""

  def get(self, request, id, *args, **kwargs):
    obj = get_object_or_404(Cotizacion,pk=id)
    obj.activo = not obj.activo
    obj.save()
    return redirect(reverse_lazy("cotizaciones-lista"))

class clienteListView(ListView):
  paginate_by = 10
  template_name = "clientes-lista.html"
  model = Cliente
  queryset = Cliente.objects.filter(activo=True)

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['btn_url'] = reverse_lazy('clientes-d-lista')
    context['btn_act'] = "Ver clientes borrados"
    return context

class empleadoListView(ListView):
  paginate_by = 10
  template_name = "empleados-lista.html"
  model = Empleado
  queryset = Empleado.objects.all()

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['btn_url'] = reverse_lazy('empleados-desactivados-lista')
    context['btn_act'] = "Ver Usuarios eliminados"
    return context

class empleadoDeactivateListView(ListView):
  paginate_by = 10
  template_name = "empleados-lista.html"
  model = Empleado
  queryset = Empleado.objects.all()

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['btn_url'] = reverse_lazy('empleados-lista')
    context['btn_act'] = "Ver Usuarios"
    context['deleted'] = True
    context['del_text'] = 'eliminados'
    return context

class empleadoDetailView(DetailView):
  template_name = "empleado-view.html"
  model = Empleado

class empleadoUpdateView(UpdateView):
  template_name = "forms.html"
  model = Empleado
  form_class = EmpleadoUpdateForm

  def get_context_data(self, **kwargs):
      context = super(UpdateView,self).get_context_data(**kwargs)
      context["tf"] =  "de actualizacion de usuarios"
      context["form"].fields["nombre"].initial = self.object.user.first_name
      context["form"].fields["apellido"].initial = self.object.user.last_name

      context["form"].fields["nombre"].disabled= True
      context["form"].fields["apellido"].disabled= True

      return context

class empleadoDeactivateView(UpdateView):
  template_name = "forms.html"
  model = Empleado
  form_class = EmpleadoUpdateForm

  def get_context_data(self, **kwargs):
      context = super(UpdateView,self).get_context_data(**kwargs)

      return context

  def get(self, request, *args, **kwargs):
    obj = self.get_object().user
    obj.is_active = not obj.is_active 
    obj.save()
    return redirect(reverse_lazy("empleados-lista"))


class clienteDetailView(DetailView):
  template_name = "cliente-view.html"
  model = Cliente

class clienteUpdateView(UpdateView):
  template_name = "forms.html"
  model = Cliente
  form_class = ClienteUpdateForm

  def get_context_data(self, **kwargs):
      context = super(UpdateView,self).get_context_data(**kwargs)
      context["tf"] =  "de actualizacion de clientes"

      return context

class clienteDeactivateListView(ListView):
  paginate_by = 10
  template_name = "clientes-lista.html"
  model = Cliente
  queryset = Cliente.objects.filter(activo=False)

  def get_context_data(self, **kwargs):
    context =  super().get_context_data(**kwargs)
    context['btn_url'] = reverse_lazy('clientes-lista')
    context['btn_act'] = "Ver clientes"
    context['Title'] = "borrados"
    context['deleted'] = "t"
    return context

class clienteDeactivateView(TemplateView):
  template_name = ""

  def get(self, request, id, *args, **kwargs):
    obj = get_object_or_404(Cliente,pk=id)
    obj.activo = not obj.activo
    obj.save()
    return redirect(reverse_lazy("clientes-lista"))

class cotizacionDetailView(DetailView):
  template_name = "cotizacion-view.html"
  model = Cotizacion

  def disable_fields(self,form):
    for field in form.fields:
      form.fields[field].disabled=True
      form.fields[field].required=False
    return

  def get_context_data(self, **kwargs):
      context = super(DetailView,self).get_context_data(**kwargs)
      context["tf"] =  "de actualizacion de cotizacion"
      context["form"] =  CotizacionUpdateForm(instance=self.object)
      context["form2"] =  ClienteForm(instance=self.object.cliente)
      context["servicios"] = Servicio.objects.filter(cotizacion=self.object)
      self.disable_fields(context["form"])
      self.disable_fields(context["form2"])
      return context

class cotizacionPrintView(DetailView):
  template_name = "cotizacion-print.html"
  model = Cotizacion

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["servicios"] = Servicio.objects.filter(cotizacion=self.object)
      return context

class cotizacionUpdateView(UpdateView):
  template_name = "crear-cotizacion.html"
  model = Cotizacion
  form_class = CotizacionUpdateForm

  def disable_fields(self,form):
    for field in form.fields:
      form.fields[field].disabled=True
      form.fields[field].required=False
    return

  def get_context_data(self, **kwargs):
      context = super(UpdateView,self).get_context_data(**kwargs)
      context["tf"] =  "de actualizacion de cotizacion"
      context["form2"] =  ClienteForm(instance=self.object.cliente)
      self.disable_fields(context["form"])
      self.disable_fields(context["form2"])
      context["formset"] =  modelformset_factory(Servicio,form=ServiciosUpdateForm,extra=0,can_delete=True)(form_kwargs={'cotizacion': self.get_object()})
      context["formset"].queryset = Servicio.objects.filter(cotizacion=self.object)

      return context

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()

    cotizacion = self.form_class(request.POST,instance=self.object)
    cliente = ClienteForm(request.POST,instance=self.object.cliente)
    self.disable_fields(cotizacion)
    self.disable_fields(cliente)

    formset = modelformset_factory(Servicio,form=ServiciosUpdateForm,extra=0,can_delete=True)
    formset = formset(request.POST,form_kwargs={'cotizacion': self.get_object()})


    # Al crear objeto no se asigna cotizacion y por ende truena
    if formset.is_valid():
      formset.save()

    else:
      context = self.get_context_data()

      return render(request, self.template_name, context)

    return redirect(reverse_lazy("cotizaciones-lista"))

def aceptar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    
    if cotizacion.estatus == 'vigente':
        cotizacion.estatus = 'ACEPTADA'
        cotizacion.save()
    
    # Redirige al usuario de regreso a la lista de cotizaciones
    return redirect('cotizaciones-lista')

def rechazar_cotizacion(request, pk):
    if request.method == 'POST':
        cotizacion = get_object_or_404(Cotizacion, pk=pk)
        comentario = request.POST.get('comentarioRechazo', '')

        if comentario:
            cotizacion.estatus = 'RECHAZADA'
            cotizacion.comentarioRechazo = comentario
            cotizacion.save()
            return redirect('cotizaciones-lista')
        else:
            return JsonResponse({'success': False, 'error': 'El comentario de rechazo es obligatorio.'})

    return JsonResponse({'success': False, 'error': 'Método no permitido.'})


class employeePasswordUpdate(TemplateView):
    template_name = 'forms.html'
    
    def get(self,request,usr,*args,**kwargs):
        context = {}
        usuario = User.objects.get(username=usr)
        
        context['form'] = UserPasswordChangeForm(usuario)
        context['tf'] = f'para actualizar contraseña de: {usuario.empleado.__str__()}'
        return render(request,self.template_name,context)

    def post(self,request,usr,*args,**kwargs):
        context = {}
        usuario = User.objects.get(username=usr)
        form = UserPasswordChangeForm(usuario,request.POST)
        context['form'] = form

        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('empleados-lista'))
        else:
            return render(request,self.template_name,context)

class CotizacionPdfView(View):
  model = Cotizacion
  model2 = Servicio
  def get (self, request, cotizacion_id, *args, **kwargs):
        cotizacion = get_object_or_404(Cotizacion, pk=cotizacion_id)
        servicios = Servicio.objects.filter(cotizacion=cotizacion)
        subtotal = sum(servicio.cantidad * servicio.precio_unitario for servicio in servicios)
        

        template = get_template('cotizaciones.html')
        context = {
           'title' : 'Resumen Cotizacion',
           'sale' : cotizacion,
           'servicios': servicios,
            'subtotal': subtotal,
           
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisa_status = pisa.CreatePDF(
          html, dest=response
          )
        # if error then show some funny view
        if pisa_status.err:
          return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

class OrdenTrabajoCreateView (TemplateView):
      template_name = 'crear-ordenTrabajo.html'
      def post(self, request, *args, **kwargs):
          form = OrdenTrabajoForm(request.POST)
          if form.is_valid():
              form.save()
              # Redirige a una página de éxito
              return redirect('ordenTrabajo-lista')
          return self.render_to_response({'form': form})

      def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['form'] = OrdenTrabajoForm()
          return context



class OrdenTrabajoListView(ListView):
    model = OrdenTrabajo
    template_name = "ordenTrabajo-lista.html"
    context_object_name = 'ordenes'  # Nombre de la variable en la plantilla
    paginate_by = 10  # Número de elementos por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn_url'] = reverse_lazy('ordenTrabajo-lista')
        return context

"""Metrotecnia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import routers
from web.api import viewsets
import web.dash
router = routers.DefaultRouter()
router.register('clientes', viewsets.ClienteViewSet)
router.register('cotizaciones', viewsets.CotizacionViewSet)
router.register('empleados', viewsets.EmpleadoViewSet)


urlpatterns = [
    path('', login_required(index.as_view()),name="index"),
    path('dash_plot', TemplateView.as_view(template_name='dash_plot.html'), name="dash_plot"),
	path('django_plotly_dash/', include('django_plotly_dash.urls')),
 
    path('dashboard',permission_required(['web.ver_dashboard'],raise_exception=True)(dashboard.as_view()), name="dashboard"),

    path('registro-cliente',permission_required(['web.ver_clientes'],raise_exception=True)(clienteCrearView.as_view()), name = "registro-cliente"),
    path('clientes-lista',permission_required(['web.ver_clientes'],raise_exception=True)(clienteListView.as_view()), name="clientes-lista"),
    path('cliente_detail/<int:pk>/',permission_required(['web.ver_clientes'],raise_exception=True)(clienteDetailView.as_view()), name="cliente_detail"),
    path('cliente-update/<int:pk>/',permission_required(['web.ver_clientes'],raise_exception=True)(clienteUpdateView.as_view()), name="cliente-update"),
    path('clientes-desactivados-lista',permission_required(['web.ver_clientes'],raise_exception=True)(clienteDeactivateListView.as_view()), name="clientes-d-lista"),
    path('clientes-deactivate/<int:id>/',permission_required(['web.ver_clientes'],raise_exception=True)(clienteDeactivateView.as_view()), name="cliente-deactivate"),

    path('crear-user',permission_required(['web.ver_usuarios'],raise_exception=True)(userCrearView.as_view()), name="crear-usuario"),
    path('empleados-lista',permission_required(['web.ver_usuarios'],raise_exception=True)(empleadoListView.as_view()), name="empleados-lista"),
    path('empleados-desactivados-lista',permission_required(['web.ver_usuarios'],raise_exception=True)(empleadoDeactivateListView.as_view()), name="empleados-desactivados-lista"),
    path('empleado_detail/<int:pk>/',permission_required(['web.ver_usuarios'],raise_exception=True)(empleadoDetailView.as_view()), name="empleado_detail"),
    path('empleado-pwd-update/<slug:usr>/',permission_required(['web.ver_usuarios'],raise_exception=True)(employeePasswordUpdate.as_view()),name='empleado-pwd-update'),    
    path('empleado-update/<int:pk>/',permission_required(['web.ver_usuarios'],raise_exception=True)(empleadoUpdateView.as_view()), name="empleado-update"),
    path('empleado-deactivate/<int:pk>/',permission_required(['web.ver_usuarios'],raise_exception=True)(empleadoDeactivateView.as_view()), name="empleado-deactivate"),

    path('crear-cotizacion',permission_required(['web.ver_cotizaciones'],raise_exception=True)(cotizacionCrearView.as_view()), name="crear-cotizacion"),
    path('cotizaciones-lista',permission_required(['web.ver_cotizaciones'],raise_exception=True)(cotizacionListView.as_view()), name="cotizaciones-lista"),
    path('cotizaciones-desactivados-lista',permission_required(['web.ver_cotizaciones'],raise_exception=True)(cotizacionDeactivateListView.as_view()), name="cotizaciones-d-lista"),
    path('cotizacion_detail/<int:pk>/',permission_required(['web.ver_cotizaciones'],raise_exception=True)(cotizacionDetailView.as_view()), name="cotizacion_detail"),
    path('cotizacion_print/<int:pk>/',permission_required(['web.ver_cotizaciones'],raise_exception=True)(cotizacionPrintView.as_view()), name="cotizacion-print"),
    path('cotizacion-update/<int:pk>/',permission_required(['web.ver_cotizaciones'],raise_exception=True)(cotizacionUpdateView.as_view()), name="cotizacion-update"),
    path('cotizacion-deactivate/<int:id>/',permission_required(['web.ver_cotizaciones'],raise_exception=True)(cotizacionDeactivateView.as_view()), name="cotizacion-deactivate"),
    path('cotizacion-pdf/<int:cotizacion_id>/', permission_required(['web.ver_cotizaciones'],raise_exception=True)(CotizacionPdfView.as_view()), name='cotizacionPdf'),

    path('crear-ordentrabajo',permission_required(['web.ver_cotizaciones'],raise_exception=True)(OrdenTrabajoCreateView.as_view()), name="crear-ordentrabajo"),
    path('ordenTrabajo-lista',permission_required(['web.ver_cotizaciones'],raise_exception=True)(OrdenTrabajoListView.as_view()), name="ordenTrabajo-lista"),


    path('', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),

]

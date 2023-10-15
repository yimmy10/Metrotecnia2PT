from rest_framework import viewsets
from web.api.serializers import *
from web.models import Cliente,Cotizacion,Empleado

class ClienteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get_queryset(self):
        out = Cliente.objects.all()
        term = self.request.GET.get("id")
        delete = self.request.GET.get("deleted")

        if term:
            out = Cliente.objects.filter(pk=term)

        out = out.filter(activo=False) if delete else out.filter(activo=True)
        return out

class CotizacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer

    def get_queryset(self):
        out = Cotizacion.objects.all()
        delete = self.request.GET.get("deleted")

        out = out.filter(activo=False) if delete else out.filter(activo=True)
        return out

class EmpleadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

    def get_queryset(self):
        out = Empleado.objects.all()
        term = self.request.GET.get("id")
        delete = self.request.GET.get("deleted")

        if term:
            out = Empleado.objects.filter(pk=term)

        out = out.filter(user__is_active=False) if delete else out.filter(user__is_active=True)
        return out
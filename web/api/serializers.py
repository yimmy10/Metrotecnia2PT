from rest_framework import serializers
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from web.models import Cliente,Cotizacion,Empleado,OrdenTrabajo


class ClienteSerializer(serializers.ModelSerializer):
    ver = serializers.SerializerMethodField()
    class Meta:
        model = Cliente
        fields = ("__all__")

    def get_ver(self,obj):
        btn_1 = f'<a class="m-1 btn btn-outline-primary" href="{reverse_lazy("cliente_detail", kwargs={"pk":obj.pk})}">Ver</a>'
        btn_2 = f"<a class='m-1 btn btn-outline-info' href='{reverse_lazy('cliente-update', kwargs={'pk':obj.pk})}'>Modificar</a>"
        btn_3 = f"<a class='m-1 btn btn-danger' href='{reverse_lazy('cliente-deactivate',kwargs={'id':obj.pk} )}'>Eliminar</a>" if obj.activo else f"<a class='m-1 btn btn-success' href='{reverse_lazy('cliente-deactivate',kwargs={'id':obj.pk} )}'>Activar</a>" 

        return f'{btn_1}{btn_2}{btn_3}' if obj.activo else f'{btn_1}{btn_3}'

class CotizacionSerializer(serializers.ModelSerializer):
    ver = serializers.SerializerMethodField()
    cliente = ClienteSerializer()
    class Meta:
        model = Cotizacion
        fields = ("__all__")

    def get_ver(self,obj):
        btn_1 = f'<a class="m-1 btn btn-outline-primary" href="{reverse_lazy("cotizacion_detail", kwargs={"pk":obj.pk})}">Ver</a>'
        btn_2 = f"<a class='m-1 btn btn-outline-info' href='{reverse_lazy('cotizacion-update', kwargs={'pk':obj.pk})}'>Modificar</a>"
        btn_3 = f"<a class='m-1 btn btn-danger' href='{reverse_lazy('cotizacion-deactivate',kwargs={'id':obj.pk} )}'>Eliminar</a>" if obj.activo else f"<a class='m-1 btn btn-success' href='{reverse_lazy('cotizacion-deactivate',kwargs={'id':obj.pk} )}'>Activar</a>" 
        btn_4 = f'<a class="m-1 btn btn-outline-danger" href="{reverse_lazy("cotizacionPdf", kwargs={"cotizacion_id": obj.pk})}">PDF</a>'
        return f'{btn_1}{btn_2}{btn_3}{btn_4}' if obj.activo and obj.estatus == "vigente" else f'{btn_1}{btn_3}'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username']

class EmpleadoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    ver = serializers.SerializerMethodField()
    class Meta:
        model = Empleado
        fields = ('__all__')
    
    def get_ver(self,obj):
        btn_1 = f'<a class="m-1 btn btn-outline-primary" href="{reverse_lazy("empleado_detail", kwargs={"pk":obj.pk})}">Ver</a>'
        btn_2 = f"<a class='m-1 btn btn-outline-info' href='{reverse_lazy('empleado-update', kwargs={'pk':obj.pk})}'>Modificar</a>"
        btn_3 = f"<a class='m-1 btn btn-outline-info' href='{reverse_lazy('empleado-pwd-update', kwargs={'usr':obj.user.username})}'>Recuperar Contraseña</a>"
        btn_4 = f"<a class='m-1 btn btn-danger' href='{reverse_lazy('empleado-deactivate',kwargs={'pk':obj.pk} )}'>Eliminar</a>" if obj.user.is_active else f"<a class='m-1 btn btn-success' href='{reverse_lazy('empleado-deactivate',kwargs={'pk':obj.pk} )}'>Activar</a>" 

        return f'{btn_1}{btn_2}{btn_3}{btn_4}' if obj.user.is_active else f'{btn_1}{btn_4}'
    

class OrdenTrabajoSerializer(serializers.ModelSerializer):
    ver = serializers.SerializerMethodField()

    class Meta:
        model = OrdenTrabajo
        fields = "__all__"

    def get_ver(self, obj):
        btn_1 = f'<a class="m-1 btn btn-outline-primary" href="{reverse_lazy("ver_orden_de_compra", kwargs={"pk": obj.pk})}">Ver</a>'
        btn_2 = f"<a class='m-1 btn btn-outline-info' href='{reverse_lazy('modificar_orden_de_compra', kwargs={'pk': obj.pk})}'>Modificar</a>"
        btn_3 = f"<a class='m-1 btn btn-danger' href='{reverse_lazy('eliminar_orden_de_compra', kwargs={'pk': obj.pk})}'>Eliminar</a>"
        btn_4 = f"<a class='m-1 btn btn-outline-danger' href='{reverse_lazy('generar_pdf_orden_de_compra', kwargs={'pk': obj.pk})}'>PDF</a>"

        return f'{btn_1}{btn_2}{btn_3}{btn_4}'




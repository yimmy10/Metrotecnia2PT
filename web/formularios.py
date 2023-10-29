from django import forms
from web.models import *
from web.widgets import ClienteWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import User, Permission

estados = [
    ("-","--- Elige Una ---"),
    ("Aguascalientes","Aguascalientes"),
    ("Baja California","Baja California"),
    ("Baja California Sur","Baja California Sur"),
    ("Campeche","Campeche"),
    ("Coahuila", "Coahuila"),
    ("Colima", "Colima"),
    ("Chiapas", "Chiapas"),
    ("Chihuahua", "Chihuahua"),
    ("Ciudad de México", "Ciudad de México"),
    ("Durango", "Durango"),
    ("Guanajuato", "Guanajuato"),
    ("Guerrero", "Guerrero"),
    ("Hidalgo", "Hidalgo"),
    ("Jalisco", "Jalisco"),
    ("Estado de México", "Estado de México"),
    ("Michoacán", "Michoacán"),
    ("Morelos", "Morelos"),
    ("Nayarit", "Nayarit"),
    ("Nuevo León", "Nuevo León"),
    ("Oaxaca", "Oaxaca"),
    ("Puebla", "Puebla"),
    ("Querétaro", "Querétaro"),
    ("Quintana Roo", "Quintana Roo"),
    ("San Luis Potosí", "San Luis Potosí"),
    ("Sinaloa", "Sinaloa"),
    ("Sonora","Sonora"),
    ("Tabasco", "Tabasco"),
    ("Tamaulipas","Tamaulipas"),
    ("Tlaxcala","Tlaxcala"),
    ("Veracruz","Veracruz"),
    ("Yucatán","Yucatán"),
    ("Zacatecas","Zacatecas")
    ]

departamentos = [
    ("-","--- Elige Una ---"),
    ("Administracion","Administracion"),
    ("Ventas","Ventas"),
    ("Cotizacion","Cotizacion"),
    ("Laboratorios","Laboratorios"),
]

TIPO_MANTTO = [
    ("-","--- Elige Una ---"),
    ("Preventivo","Preventivo"),
    ("Correctivo","Correctivo"),
    ("Cambio de Presion de Ajuste","Cambio de Presion de Ajuste"),
]

P_AJUSTE = [
    ("-","--- Elige Una ---"),
    ("PSI","PSI"),
    ("KPA","KPA"),
    ("VAR","VAR"),
    ("KG/CM2","KG/CM2"),
]

ENTRADA_NOMINAL = [
    ("-","--- Elige Una ---"),
    ("3.2 mm  (1/8')","3.2 mm  (1/8')"),
    ("6 mm  (1/4')","6 mm  (1/4')"),
    ("9 mm  (3/8')","9 mm  (3/8')"),
    ("12 mm ","12 mm"),
    ("13 mm ( 1/2' ) ","13mm ( 1/2' )"),
    ("19 mm ( 3/4' ) ","19mm ( 3/4' )"),
    ("25 mm ( 1' ) ","25 mm ( 1' )"),
    ("32 mm ( 1 1/4' ) ","32 mm ( 1 1/4' )"),
    ("38 mm ( 1 1/2' ) ","38 mm ( 1 1/2' )"),
    ("44 mm ( 1 3/4' ) ","44 mm ( 1 3/4' )"),
    ("51 mm ( 2' ) ","51 mm ( 2' )"),
    ("57 mm ( 2 1/4' ) ","57 mm ( 2 1/4' )"),
    ("63 mm ( 2 1/2' ) ","63 mm ( 2 1/2' )"),
    ("64 mm","64 mm"),
    ("75 mm ( 3' ) ","75 mm ( 3' )"),
    ("100 mm ( 4' ) ","100 mm ( 4' )"),
    ("Orificios en el cuerpo ","Orificios en el cuerpo"),
]

CONDICION =[
    ("-","--- Elige Una ---"),
    ("Nueva","Nueva"),
    ("En uso","En uso"),
    ("Desconocida","Desconocida"),
]

PRUEBA = [
    ("-","--- Elige Una ---"),
    ("Ajuste","Ajuste"),
    ("Ajuste - Hermicidad","Ajuste - Hermicidad"),
    ("Ajuste - Hermicidad - Néumatica","Ajuste - Hermicidad - Néumatica"),
]

CONDICIONES_PAGO = [
    ("-","--- Elige Una ---"),
    ("Anticipado","Anticipado"),
    ("Contra aviso de entrega","Contra aiso de entrega"),
    ("Credito a X días","Credito a X días"),
]


class ClienteForm(forms.ModelForm):
    estado = forms.ChoiceField(choices=estados)
    field_order = ["clientes",'razon_social','rfc','calle_numero_colonia','ciudad','estado','cp','Contacto','correo','telefono']

    class  Meta:
        model = Cliente
        exclude = ['activo',]

        labels = {
            "razon_social": "Razón Social",
            "rfc": "RFC",
            "calle_numero_colonia": "Dirección",
            "ciudad": "Ciudad",
            "estado": "Estado",
            "cp": "C.P.",
            "Contacto": "Contacto",
            "correo": "Correo",
            "telefono": "Teléfono"
        }

class ClienteOrdenForm(forms.ModelForm):
    clientes = forms.ModelChoiceField(queryset=Cliente.objects.filter(activo=True).order_by('razon_social'),required=False,widget=ClienteWidget(attrs={'data-placeholder': 'Buscar un cliente', 'data-width': '100%'}))
    estado = forms.ChoiceField(choices=estados)
    field_order = ["clientes",'razon_social','rfc','calle_numero_colonia','ciudad','estado','cp','Contacto','correo','telefono']
    class  Meta:
        model = Cliente
        exclude = ['activo',]

        labels = {
            "razon_social": "Razón Social",
            "rfc": "RFC",
            "calle_numero_colonia": "Calle/Número/Colonia",
            "ciudad": "Ciudad",
            "estado": "Estado",
            "cp": "C.P.",
            "Contacto": "Contacto",
            "correo": "Correo",
            "telefono": "Teléfono"
        }
        
class CotizacionForm(forms.ModelForm):
    condiciones = forms.ChoiceField(label="Condiciones de pago",choices=CONDICIONES_PAGO)

    class Meta:
        model = Cotizacion
        exclude = [
            "cliente",
            'activo',
            'estatus',
            'comentarioRechazo',
        ]

        labels = {
            "fecha_entrega": "Tiempo de entrega",
            "condiciones": "Condiciones de pago",
            "codigo": "Código"
        }

class EmpleadoForm(UserCreationForm):
    nombre = forms.CharField(max_length=60)
    apellido = forms.CharField(max_length=60)
    puesto = forms.CharField(max_length=60)
    departamento = forms.ChoiceField(choices=departamentos)
    telefono = forms.CharField(max_length=60,label="Teléfono")
    direccion = forms.CharField(max_length=60,label="Dirección")

    def save(self, commit=True):
        clientes = Permission.objects.get(codename='ver_clientes')
        usuarios = Permission.objects.get(codename='ver_usuarios')
        cotizaciones = Permission.objects.get(codename='ver_cotizaciones')
        dashboard = Permission.objects.get(codename='ver_dashboard')
        usr = super(UserCreationForm,self).save(commit)
        usr.first_name = self.cleaned_data.get("nombre")
        usr.last_name = self.cleaned_data.get("apellido")
        puesto = self.cleaned_data.get("puesto")
        departamento = self.cleaned_data.get("departamento")
        if departamento == "Administracion":
            usr.user_permissions.set([clientes,usuarios,cotizaciones,dashboard])

        elif departamento == "Ventas" or departamento == "Cotizacion":
            usr.user_permissions.set([clientes,cotizaciones])

        elif departamento == "Laboratorios":
            usr.user_permissions.set([cotizaciones])

        telefono = self.cleaned_data.get("telefono")
        direccion = self.cleaned_data.get("direccion")
        obj = Empleado(puesto=puesto,departamento=departamento,telefono=telefono,direccion=direccion,user=usr)
        obj.save()
        usr.save()
        return usr


class EmpleadoUpdateForm(forms.ModelForm):
    nombre = forms.CharField(max_length=60,required=False)
    apellido = forms.CharField(max_length=60,required=False)
    departamento = forms.ChoiceField(choices=departamentos)

    class Meta:
        model = Empleado
        exclude = ("user",'activo')

    field_order = ['nombre', 'apellido', 'departamento', 'puesto', 'telefono', 'direccion']

    def save(self, commit=True):
        obj = super(EmpleadoUpdateForm,self).save(commit)
        usr = self.instance.user
        clientes = Permission.objects.get(codename='ver_clientes')
        usuarios = Permission.objects.get(codename='ver_usuarios')
        cotizaciones = Permission.objects.get(codename='ver_cotizaciones')
        dashboard = Permission.objects.get(codename='ver_dashboard')
        departamento = self.cleaned_data.get("departamento")
        
        if departamento == "Administracion":
            usr.user_permissions.set([clientes,usuarios,cotizaciones,dashboard])

        elif departamento == "Ventas" or departamento == "Cotizacion":
            usr.user_permissions.set([clientes,cotizaciones])

        elif departamento == "Laboratorios":
            usr.user_permissions.set([cotizaciones])
        return obj



class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicio
        exclude = ['cotizacion','active','n_serie','id_valvula','agua','vapor','p_ajuste_dc','p_hermeticidad','p_neumatica','mantto_preventivo','mantto_correctivo','cambio_p_ajuste','acreditado','otro_servicio','version_original']
        widgets = {
            'tipo_mantenimiento': forms.Select(choices=TIPO_MANTTO),
            'entrada_nominal': forms.Select(choices=ENTRADA_NOMINAL),
            'ajuste': forms.Select(choices=P_AJUSTE),
            'condicion': forms.Select(choices=CONDICION),
            'prueba': forms.Select(choices=PRUEBA),
        }
        labels ={
            'condicion': "Condición",

        }
 
class ServiciosUpdateForm(forms.ModelForm):

    class Meta:
        model = Servicio
        exclude = ['cotizacion','active','version_original','mantto_preventivo','mantto_correctivo','cambio_p_ajuste']
        widgets = {
            'tipo_mantenimiento': forms.Select(choices=TIPO_MANTTO),
            'entrada_nominal': forms.Select(choices=ENTRADA_NOMINAL),
            'ajuste': forms.Select(choices=P_AJUSTE),
            'condicion': forms.Select(choices=CONDICION),
            'prueba': forms.Select(choices=PRUEBA),
        }

    def __init__(self, *args, **kwargs):
        self.cotizacion = kwargs.pop('cotizacion')
        super(ServiciosUpdateForm, self).__init__(*args, **kwargs)

    def save(self,*args, **kwargs):
        obj = super(ServiciosUpdateForm,self).save(commit=False)
        obj.cotizacion = self.cotizacion
        obj.save()
        return obj

class ClienteUpdateForm(forms.ModelForm):
    # nombre = forms.CharField(max_length=60,required=False)
    # apellido = forms.CharField(max_length=60,required=False)
    estado = forms.ChoiceField(choices=estados)


    class Meta:
        model = Cliente
        fields = ("razon_social", "rfc", "calle_numero_colonia", "ciudad", "estado", "cp", "contacto", "correo", "telefono",)
        # exclude = ("user",)

    # field_order = ['nombre', 'apellido', 'departamento', 'puesto', 'telefono', 'direccion']

class CotizacionUpdateForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = "__all__"
        labels = {
            'fecha_entrega': 'Tiempo de entrega',
            'comentarioRechazo': 'Comentario de rechazo'
        }

    def __init__(self, *args, **kwargs):
        super(CotizacionUpdateForm, self).__init__(*args, **kwargs)

        # Obtén el valor actual de estatus
        estatus_actual = self.instance.estatus

        # Personaliza los campos basados en el valor de estatus
        if estatus_actual != "RECHAZADA":
            self.fields['comentarioRechazo'].widget = forms.HiddenInput()
            self.fields['estatus'].widget = forms.HiddenInput()
        else:
            self.fields['comentarioRechazo'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 50})
            self.fields['estatus'].widget = forms.HiddenInput()

class UserPasswordChangeForm(AdminPasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)


class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = [
            "codigoOT",
            "nombre",
            "fecha",
            "declaraconf",
            "ordenCompra",
            "notas",
            "serie",
            "id_Product",  # Agregamos el campo id_Product
            "notas_especiales",
            "cotizacion_id"
        ]
        labels = {
            "codigoOT": "Codigo OT",
            "nombre": "Nombre",
            "fecha": "Fecha",
            "declaraconf": "Declaración de confidencialidad",
            "ordenCompra": "Orden de compra",
            "notas": "Notas",
            "serie": "Serie",
            "id_Product": "ID del Producto",  # Etiqueta personalizada para id_Product
            "notas_especiales": "Notas especiales",
            "cotizacion_id": "Cotización"
        }
    def __init__(self, *args, **kwargs):
        super(OrdenTrabajoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        # Asignar un widget de checkbox al campo "declaraconf"
        self.fields['declaraconf'].widget = forms.CheckboxInput()
        self.fields['fecha'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        self.fields['notas'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        self.fields['notas_especiales'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        self.fields['cotizacion_id'].queryset = Cotizacion.objects.filter(estatus='ACEPTADA')









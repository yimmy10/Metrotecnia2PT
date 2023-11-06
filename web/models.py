from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    razon_social = models.CharField(max_length=100)
    rfc = models.CharField(max_length=20)
    calle_numero_colonia = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    estado = models.TextField()
    cp = models.IntegerField()
    contacto = models.CharField(max_length=70)
    correo = models.EmailField()
    telefono = models.CharField(max_length=14)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("cliente")
        verbose_name_plural = ("clientes")

    def __str__(self):
        return self.razon_social

    def get_absolute_url(self):
        return reverse("cliente_detail", kwargs={"pk": self.pk})

class Empleado(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=150)
    departamento = models.CharField(max_length=150)
    telefono = models.CharField(max_length=14)
    direccion = models.CharField(max_length=150)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("Empleado")
        verbose_name_plural = ("Empleados")
        permissions = [
            ('ver_clientes','Ver Clientes'),
            ('ver_cotizaciones','Ver Cotizaciones'),
            ('ver_usuarios','Ver Usuarios'),
            ('ver_dashboard','Ver Dashboard'),
        ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def get_absolute_url(self):
        return reverse("empleado_detail", kwargs={"pk": self.pk})
    
VIGENTE = 'VIGENTE'
ACEPTADA = 'ACEPTADA'
RECHAZADA = 'RECHAZADA'
STATUS_CHOICES = (
    (VIGENTE, 'vigente'),
    (ACEPTADA, 'aceptada'),
    (RECHAZADA, 'rechazada'),
)

class Cotizacion(models.Model):

    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, auto_now_add=False)
    cotizado_por = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    solicitud = models.CharField(max_length=15)
    codigo = models.CharField(max_length=15)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_entrega = models.IntegerField()
    condiciones = models.CharField(max_length=100)
    notas_especiales = models.CharField(max_length=100,blank=True,null=True)
    notas_internas = models.CharField(max_length=100,blank=True,null=True)
    urgente =  models.BooleanField(default=0)
    activo = models.BooleanField(default=True)
    estatus = models.CharField(max_length=255, default='VIGENTE', choices=STATUS_CHOICES)
    comentarioRechazo = models.CharField(max_length=255,blank=True, null=True)

    class Meta:
        verbose_name = ("Cotizacion")
        verbose_name_plural = ("Cotizacions")

    def __str__(self):
        return self.pk.__str__()
    
class Servicio(models.Model):

    cantidad =  models.IntegerField()
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    valor_ajuste = models.DecimalField(max_digits=16, decimal_places=2)
    ajuste = models.CharField(max_length=100)
    entrada_nominal = models.CharField(max_length=100)
    caldera = models.BooleanField(default=0)
    condicion = models.CharField(max_length=100)
    prueba = models.CharField(max_length=100)
    alcance_acreditado = models.BooleanField(default=1)
    notas = models.CharField(max_length=100,blank=True,null=True)
    precio_unitario = models.DecimalField(max_digits=16, decimal_places=2)
    mantenimiento = models.BooleanField()
    tipo_mantenimiento = models.CharField(max_length=100,blank=True,null=True)
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    version_original = models.IntegerField(default=1)
    active = models.BooleanField(default=1)
    n_serie = models.CharField(max_length=50,blank=True)
    id_valvula = models.CharField(max_length=50,blank=True)
    agua = models.BooleanField(default=0)
    vapor = models.BooleanField(default=0)
    p_ajuste_dc = models.BooleanField(default=0)
    p_hermeticidad = models.BooleanField(default=0)
    p_neumatica = models.BooleanField(default=0)
    mantto_preventivo = models.BooleanField(default=0)
    mantto_correctivo = models.BooleanField(default=0)
    cambio_p_ajuste = models.BooleanField(default=0)
    acreditado = models.BooleanField(default=0)
    otro_servicio = models.BooleanField(default=0)


    class Meta:
        verbose_name = ("Servicio")
        verbose_name_plural = ("Servicios")

    def __str__(self):
        return self.pk.__str__()

class ServicioEspecial(models.Model):

    cantidad =  models.IntegerField()
    concepto =  models.TextField()
    notas = models.TextField()
    precio_unitario = models.DecimalField(max_digits=16, decimal_places=2)
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    version_original = models.IntegerField(default=1)
    active = models.BooleanField(default=1)

    class Meta:
        verbose_name = ("Libre")
        verbose_name_plural = ("Libres")

    def __str__(self):
        return self.pk

ESPERA = 'ESPERA'
LABORATORIO = 'LABORATORIO'
REVISION = 'REVISION'
TERMINADO = 'TERMINADO'
PAUSA = 'PAUSA'
STATUS_ORDEN = (
    (ESPERA, 'ESPERA'),
    (LABORATORIO, 'LABORATORIO'),
    (REVISION, 'REVISION'),
    (TERMINADO, 'TERMINADO'),
    (PAUSA, 'PAUSA'),
)
class OrdenTrabajo(models.Model):
    codigoOT = models.CharField(max_length = 255)
    nombre = models.CharField(max_length=255)
    fecha = models.DateField()
    declaraconf = models.BooleanField(default=0)
    ordenCompra = models.IntegerField()
    notas = models.CharField(max_length = 255)
    serie = models.CharField(max_length = 255)
    id_Product = models.CharField(max_length = 255)
    notas_especiales = models.CharField(max_length = 255)
    cotizacion_id = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    estatus = models.CharField(max_length=255, default='ESPERA', choices=STATUS_ORDEN)
    comentarioRechazo = models.CharField(max_length=255,blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = ("OrdenTrabajo")
        verbose_name_plural = ("OrdenTrabajos")

    def _str_(self):
        return self.pk._str_()
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class Empresa(models.Model):
    """Modelo para registrar empresas cliente"""
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    rut = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=300, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    contacto_principal = models.CharField(max_length=200, blank=True, null=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    """Modelo para registrar equipos de las empresas"""
    ESTADO_CHOICES = [
        ('operativo', 'Operativo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('reparacion', 'En Reparación'),
        ('fuera_servicio', 'Fuera de Servicio'),
        ('inactivo', 'Inactivo'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='equipos')
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=100)  # Ej: Bomba, Motor, Compresor
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    serie = models.CharField(max_length=100, blank=True, null=True)
    ubicacion = models.CharField(max_length=300, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='operativo')
    fecha_adquisicion = models.DateField(blank=True, null=True)
    fecha_instalacion = models.DateField(blank=True, null=True)
    fecha_ultimo_mantenimiento = models.DateField(blank=True, null=True)
    critical = models.BooleanField(default=False, help_text="Indica si es equipo crítico")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['empresa', 'nombre']
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        unique_together = ('empresa', 'codigo')

    def __str__(self):
        return f"{self.nombre} ({self.codigo}) - {self.empresa.nombre}"


class Tecnico(models.Model):
    """Modelo para registrar técnicos de mantenimiento"""
    ESPECIALIDAD_CHOICES = [
        ('mecanico', 'Mecánico'),
        ('electrico', 'Eléctrico'),
        ('hidraulico', 'Hidráulico'),
        ('electromecanico', 'Electromecánico'),
        ('general', 'General'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    rut = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    especialidad = models.CharField(max_length=20, choices=ESPECIALIDAD_CHOICES)
    experiencia_anos = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )
    certificaciones = models.TextField(blank=True, null=True)
    empresas = models.ManyToManyField(Empresa, related_name='tecnicos', blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tecnico')
    activo = models.BooleanField(default=True)
    fecha_contratacion = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'Técnico'
        verbose_name_plural = 'Técnicos'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.get_especialidad_display()}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Plan(models.Model):
    """Modelo para planes de mantenimiento"""
    FRECUENCIA_CHOICES = [
        ('diaria', 'Diaria'),
        ('semanal', 'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
        ('otro', 'Otro'),
    ]

    TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('predictivo', 'Predictivo'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='planes')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='planes')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='preventivo')
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES)
    frequency_days = models.IntegerField(default=30, help_text="Frecuencia en días")
    duracion_estimada_horas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=1
    )
    tareas = models.TextField()  # Descripción de las tareas a realizar
    herramientas_requeridas = models.TextField(blank=True, null=True)
    repuestos_comunes = models.TextField(blank=True, null=True)
    tecnicos_recomendados = models.ManyToManyField(Tecnico, related_name='planes', blank=True)
    costo_estimado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField()
    fecha_proximo_mantenimiento = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['empresa', 'equipo', 'nombre']
        verbose_name = 'Plan de Mantenimiento'
        verbose_name_plural = 'Planes de Mantenimiento'
        unique_together = ('equipo', 'nombre')

    def __str__(self):
        return f"{self.nombre} - {self.equipo.nombre}"


class Orden(models.Model):
    """Modelo para órdenes de trabajo"""
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('en_progreso', 'En Progreso'),
        ('pausada', 'Pausada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('pendiente', 'Pendiente'),
    ]

    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='ordenes')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='ordenes')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes')
    tecnico_asignado = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes')
    numero_orden = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='media')
    fecha_programada = models.DateTimeField()
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_termino = models.DateTimeField(blank=True, null=True)
    horas_trabajadas = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    observaciones = models.TextField(blank=True, null=True)
    repuestos_utilizados = models.TextField(blank=True, null=True)
    costo_real = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_programada']
        verbose_name = 'Orden de Trabajo'
        verbose_name_plural = 'Órdenes de Trabajo'

    def __str__(self):
        return f"{self.numero_orden} - {self.equipo.nombre}"

    def save(self, *args, **kwargs):
        if not self.numero_orden:
            # Generar número de orden automáticamente
            ultimo = Orden.objects.order_by('-id').first()
            numero = 1 if not ultimo else (int(ultimo.numero_orden.split('-')[-1]) + 1)
            self.numero_orden = f"ORD-{timezone.now().year}-{numero:05d}"
        super().save(*args, **kwargs)

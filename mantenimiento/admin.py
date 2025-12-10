from django.contrib import admin
from .models import Empresa, Equipo, Tecnico, Plan, Orden


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'email', 'ciudad', 'activa', 'fecha_creacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre', 'rut', 'email']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'rut', 'descripcion')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'contacto_principal')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'ciudad')
        }),
        ('Estado', {
            'fields': ('activa',)
        }),
        ('Timestamps', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'empresa', 'tipo', 'estado', 'fecha_ultimo_mantenimiento']
    list_filter = ['estado', 'tipo', 'empresa', 'fecha_creacion']
    search_fields = ['nombre', 'codigo', 'serie']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('empresa', 'nombre', 'codigo', 'descripcion')
        }),
        ('Especificaciones', {
            'fields': ('tipo', 'marca', 'modelo', 'serie')
        }),
        ('Ubicación y Estado', {
            'fields': ('ubicacion', 'estado')
        }),
        ('Fechas Importantes', {
            'fields': ('fecha_adquisicion', 'fecha_instalacion', 'fecha_ultimo_mantenimiento')
        }),
        ('Estado Operativo', {
            'fields': ('activo',)
        }),
        ('Timestamps', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'rut', 'especialidad', 'email', 'experiencia_anos', 'activo']
    list_filter = ['especialidad', 'activo', 'fecha_contratacion']
    search_fields = ['nombre', 'apellido', 'rut', 'email']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    filter_horizontal = ['empresas']
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'rut', 'email', 'telefono')
        }),
        ('Profesional', {
            'fields': ('especialidad', 'experiencia_anos', 'certificaciones')
        }),
        ('Asignaciones', {
            'fields': ('empresas',)
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_contratacion')
        }),
        ('Timestamps', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'equipo', 'tipo', 'frecuencia', 'activo', 'fecha_proximo_mantenimiento']
    list_filter = ['tipo', 'frecuencia', 'activo', 'empresa']
    search_fields = ['nombre', 'equipo__nombre', 'tareas']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    filter_horizontal = ['tecnicos_recomendados']
    fieldsets = (
        ('Información Básica', {
            'fields': ('empresa', 'equipo', 'nombre', 'descripcion')
        }),
        ('Configuración del Plan', {
            'fields': ('tipo', 'frecuencia', 'duracion_estimada_horas')
        }),
        ('Detalles Técnicos', {
            'fields': ('tareas', 'herramientas_requeridas', 'repuestos_comunes')
        }),
        ('Recursos', {
            'fields': ('tecnicos_recomendados', 'costo_estimado')
        }),
        ('Programación', {
            'fields': ('activo', 'fecha_inicio', 'fecha_proximo_mantenimiento')
        }),
        ('Timestamps', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'equipo', 'tecnico_asignado', 'estado', 'prioridad', 'fecha_programada']
    list_filter = ['estado', 'prioridad', 'empresa', 'fecha_programada']
    search_fields = ['numero_orden', 'equipo__nombre', 'descripcion']
    readonly_fields = ['numero_orden', 'fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('numero_orden', 'empresa', 'equipo', 'plan')
        }),
        ('Descripción', {
            'fields': ('descripcion', 'observaciones')
        }),
        ('Asignación', {
            'fields': ('tecnico_asignado',)
        }),
        ('Estado y Prioridad', {
            'fields': ('estado', 'prioridad')
        }),
        ('Programación', {
            'fields': ('fecha_programada', 'fecha_inicio', 'fecha_termino')
        }),
        ('Detalles de Ejecución', {
            'fields': ('horas_trabajadas', 'repuestos_utilizados', 'costo_real')
        }),
        ('Timestamps', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

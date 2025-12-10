from rest_framework import serializers
from .models import Empresa, Equipo, Tecnico, Plan, Orden


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Empresa"""
    class Meta:
        model = Empresa
        fields = [
            'id', 'nombre', 'descripcion', 'rut', 'telefono', 'email',
            'direccion', 'ciudad', 'contacto_principal', 'activa',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']


class EmpresaDetailSerializer(EmpresaSerializer):
    """Serializador detallado de Empresa con relaciones"""
    equipos = serializers.SerializerMethodField()
    planes = serializers.SerializerMethodField()
    ordenes = serializers.SerializerMethodField()
    
    class Meta(EmpresaSerializer.Meta):
        fields = EmpresaSerializer.Meta.fields + ['equipos', 'planes', 'ordenes']
    
    def get_equipos(self, obj):
        equipos = obj.equipos.all()
        return EquipoSerializer(equipos, many=True).data
    
    def get_planes(self, obj):
        planes = obj.planes.all()
        return PlanSerializer(planes, many=True).data
    
    def get_ordenes(self, obj):
        ordenes = obj.ordenes.all()[:10]  # Últimas 10 órdenes
        return OrdenListSerializer(ordenes, many=True).data


class EquipoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Equipo"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Equipo
        fields = [
            'id', 'empresa', 'empresa_nombre', 'nombre', 'codigo', 'descripcion',
            'tipo', 'marca', 'modelo', 'serie', 'ubicacion', 'estado',
            'estado_display', 'fecha_adquisicion', 'fecha_instalacion',
            'fecha_ultimo_mantenimiento', 'activo', 'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']


class EquipoDetailSerializer(EquipoSerializer):
    """Serializador detallado de Equipo con relaciones"""
    planes = serializers.SerializerMethodField()
    ordenes = serializers.SerializerMethodField()
    
    class Meta(EquipoSerializer.Meta):
        fields = EquipoSerializer.Meta.fields + ['planes', 'ordenes']
    
    def get_planes(self, obj):
        planes = obj.planes.all()
        return PlanSerializer(planes, many=True).data
    
    def get_ordenes(self, obj):
        ordenes = obj.ordenes.all()[:10]
        return OrdenListSerializer(ordenes, many=True).data


class TecnicoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Técnico"""
    especialidad_display = serializers.CharField(source='get_especialidad_display', read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Tecnico
        fields = [
            'id', 'nombre', 'apellido', 'nombre_completo', 'rut', 'email',
            'telefono', 'especialidad', 'especialidad_display', 'experiencia_anos',
            'certificaciones', 'activo', 'fecha_contratacion', 'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion', 'nombre_completo']


class TecnicoDetailSerializer(TecnicoSerializer):
    """Serializador detallado de Técnico con relaciones"""
    empresas = EmpresaSerializer(many=True, read_only=True)
    ordenes = serializers.SerializerMethodField()
    
    class Meta(TecnicoSerializer.Meta):
        fields = TecnicoSerializer.Meta.fields + ['empresas', 'ordenes']
    
    def get_ordenes(self, obj):
        ordenes = obj.ordenes.all()[:10]
        return OrdenListSerializer(ordenes, many=True).data


class PlanSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Plan"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    equipo_nombre = serializers.CharField(source='equipo.nombre', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    frecuencia_display = serializers.CharField(source='get_frecuencia_display', read_only=True)
    
    class Meta:
        model = Plan
        fields = [
            'id', 'empresa', 'empresa_nombre', 'equipo', 'equipo_nombre',
            'nombre', 'descripcion', 'tipo', 'tipo_display', 'frecuencia',
            'frecuencia_display', 'duracion_estimada_horas', 'tareas',
            'herramientas_requeridas', 'repuestos_comunes', 'costo_estimado',
            'activo', 'fecha_inicio', 'fecha_proximo_mantenimiento',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']


class PlanDetailSerializer(PlanSerializer):
    """Serializador detallado de Plan con relaciones"""
    tecnicos_recomendados = TecnicoSerializer(many=True, read_only=True)
    ordenes = serializers.SerializerMethodField()
    
    class Meta(PlanSerializer.Meta):
        fields = PlanSerializer.Meta.fields + ['tecnicos_recomendados', 'ordenes']
    
    def get_ordenes(self, obj):
        ordenes = obj.ordenes.all()[:10]
        return OrdenListSerializer(ordenes, many=True).data


class OrdenListSerializer(serializers.ModelSerializer):
    """Serializador simplificado para Orden (usado en listas)"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    equipo_nombre = serializers.CharField(source='equipo.nombre', read_only=True)
    tecnico_nombre = serializers.CharField(source='tecnico_asignado.nombre_completo', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    prioridad_display = serializers.CharField(source='get_prioridad_display', read_only=True)
    
    class Meta:
        model = Orden
        fields = [
            'id', 'numero_orden', 'empresa', 'empresa_nombre', 'equipo',
            'equipo_nombre', 'tecnico_asignado', 'tecnico_nombre', 'estado',
            'estado_display', 'prioridad', 'prioridad_display', 'fecha_programada',
            'fecha_inicio', 'fecha_termino', 'horas_trabajadas'
        ]
        read_only_fields = ['id', 'numero_orden']


class OrdenSerializer(serializers.ModelSerializer):
    """Serializador completo para Orden"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    equipo_nombre = serializers.CharField(source='equipo.nombre', read_only=True)
    plan_nombre = serializers.CharField(source='plan.nombre', read_only=True, allow_null=True)
    tecnico_nombre = serializers.CharField(source='tecnico_asignado.nombre_completo', read_only=True, allow_null=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    prioridad_display = serializers.CharField(source='get_prioridad_display', read_only=True)
    
    class Meta:
        model = Orden
        fields = [
            'id', 'numero_orden', 'empresa', 'empresa_nombre', 'equipo',
            'equipo_nombre', 'plan', 'plan_nombre', 'tecnico_asignado',
            'tecnico_nombre', 'descripcion', 'estado', 'estado_display',
            'prioridad', 'prioridad_display', 'fecha_programada', 'fecha_inicio',
            'fecha_termino', 'horas_trabajadas', 'observaciones', 'repuestos_utilizados',
            'costo_real', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'numero_orden', 'fecha_creacion', 'fecha_actualizacion']


class OrdenDetailSerializer(OrdenSerializer):
    """Serializador detallado de Orden con todas las relaciones"""
    empresa = EmpresaSerializer(read_only=True)
    equipo = EquipoSerializer(read_only=True)
    plan = PlanSerializer(read_only=True, allow_null=True)
    tecnico_asignado = TecnicoSerializer(read_only=True, allow_null=True)
    
    class Meta(OrdenSerializer.Meta):
        fields = OrdenSerializer.Meta.fields + ['empresa', 'equipo', 'plan', 'tecnico_asignado']


class OrdenCrearActualizarSerializer(serializers.ModelSerializer):
    """Serializador para crear y actualizar Órdenes"""
    class Meta:
        model = Orden
        fields = [
            'empresa', 'equipo', 'plan', 'tecnico_asignado', 'descripcion',
            'estado', 'prioridad', 'fecha_programada', 'fecha_inicio',
            'fecha_termino', 'horas_trabajadas', 'observaciones',
            'repuestos_utilizados', 'costo_real'
        ]
    
    def validate(self, data):
        """Validaciones customizadas"""
        empresa = data.get('empresa')
        equipo = data.get('equipo')
        
        # Verificar que el equipo pertenece a la empresa
        if equipo and empresa and equipo.empresa != empresa:
            raise serializers.ValidationError(
                "El equipo seleccionado no pertenece a la empresa especificada."
            )
        
        # Validar fechas
        fecha_inicio = data.get('fecha_inicio')
        fecha_termino = data.get('fecha_termino')
        
        if fecha_inicio and fecha_termino and fecha_inicio > fecha_termino:
            raise serializers.ValidationError(
                "La fecha de inicio no puede ser posterior a la fecha de término."
            )
        
        # Validar horas trabajadas positivas
        horas = data.get('horas_trabajadas')
        if horas and horas < 0:
            raise serializers.ValidationError(
                "Las horas trabajadas no pueden ser negativas."
            )
        
        return data


class EstadisticasEmpresaSerializer(serializers.Serializer):
    """Serializador para estadísticas de empresa"""
    total_equipos = serializers.IntegerField()
    total_planes = serializers.IntegerField()
    total_ordenes = serializers.IntegerField()
    ordenes_pendientes = serializers.IntegerField()
    ordenes_en_progreso = serializers.IntegerField()
    ordenes_completadas = serializers.IntegerField()
    costo_total_ordenes = serializers.DecimalField(max_digits=12, decimal_places=2)
    horas_totales_trabajadas = serializers.DecimalField(max_digits=10, decimal_places=2)


class EstadisticasEquipoSerializer(serializers.Serializer):
    """Serializador para estadísticas de equipo"""
    nombre_equipo = serializers.CharField()
    total_ordenes = serializers.IntegerField()
    ordenes_completadas = serializers.IntegerField()
    dias_sin_mantenimiento = serializers.IntegerField()
    proxima_mantencion = serializers.DateField()
    costo_total_mantenimiento = serializers.DecimalField(max_digits=12, decimal_places=2)
    horas_totales_trabajadas = serializers.DecimalField(max_digits=10, decimal_places=2)

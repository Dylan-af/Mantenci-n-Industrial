from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from .models import Empresa, Equipo, Tecnico, Plan, Orden
from .serializers import (
    EmpresaSerializer, EmpresaDetailSerializer,
    EquipoSerializer, EquipoDetailSerializer,
    TecnicoSerializer, TecnicoDetailSerializer,
    PlanSerializer, PlanDetailSerializer,
    OrdenListSerializer, OrdenSerializer, OrdenDetailSerializer,
    OrdenCrearActualizarSerializer,
    EstadisticasEmpresaSerializer, EstadisticasEquipoSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Empresas.
    
    Métodos disponibles:
    - GET /empresas/ - Listar todas las empresas
    - POST /empresas/ - Crear nueva empresa
    - GET /empresas/{id}/ - Obtener detalles de empresa
    - PUT /empresas/{id}/ - Actualizar empresa
    - DELETE /empresas/{id}/ - Eliminar empresa
    - GET /empresas/{id}/estadisticas/ - Obtener estadísticas
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'rut', 'email', 'ciudad']
    ordering_fields = ['nombre', 'fecha_creacion']
    ordering = ['-fecha_creacion']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmpresaDetailSerializer
        return EmpresaSerializer

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtener estadísticas de la empresa"""
        empresa = self.get_object()
        
        ordenes = empresa.ordenes.all()
        
        estadisticas = {
            'total_equipos': empresa.equipos.count(),
            'total_planes': empresa.planes.count(),
            'total_ordenes': ordenes.count(),
            'ordenes_pendientes': ordenes.filter(estado='programada').count(),
            'ordenes_en_progreso': ordenes.filter(estado='en_progreso').count(),
            'ordenes_completadas': ordenes.filter(estado='completada').count(),
            'costo_total_ordenes': ordenes.aggregate(Sum('costo_real'))['costo_real__sum'] or 0,
            'horas_totales_trabajadas': ordenes.aggregate(Sum('horas_trabajadas'))['horas_trabajadas__sum'] or 0,
        }
        
        serializer = EstadisticasEmpresaSerializer(estadisticas)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Obtener solo empresas activas"""
        empresas = self.queryset.filter(activa=True)
        page = self.paginate_queryset(empresas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(empresas, many=True)
        return Response(serializer.data)


class EquipoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Equipos.
    
    Métodos disponibles:
    - GET /equipos/ - Listar todos los equipos
    - POST /equipos/ - Crear nuevo equipo
    - GET /equipos/{id}/ - Obtener detalles del equipo
    - PUT /equipos/{id}/ - Actualizar equipo
    - DELETE /equipos/{id}/ - Eliminar equipo
    - GET /equipos/{id}/estadisticas/ - Estadísticas del equipo
    - GET /equipos/por-empresa/{empresa_id}/ - Equipos por empresa
    """
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'codigo', 'tipo', 'marca']
    ordering_fields = ['nombre', 'estado', 'fecha_ultimo_mantenimiento']
    ordering = ['-fecha_creacion']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EquipoDetailSerializer
        return EquipoSerializer

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtener estadísticas del equipo"""
        equipo = self.get_object()
        ordenes = equipo.ordenes.all()
        
        fecha_proximo = equipo.planes.filter(
            activo=True
        ).values_list('fecha_proximo_mantenimiento', flat=True).first()
        
        dias_sin_mantenimiento = 0
        if equipo.fecha_ultimo_mantenimiento:
            dias_sin_mantenimiento = (timezone.now().date() - equipo.fecha_ultimo_mantenimiento).days
        
        estadisticas = {
            'nombre_equipo': equipo.nombre,
            'total_ordenes': ordenes.count(),
            'ordenes_completadas': ordenes.filter(estado='completada').count(),
            'dias_sin_mantenimiento': dias_sin_mantenimiento,
            'proxima_mantencion': fecha_proximo,
            'costo_total_mantenimiento': ordenes.aggregate(Sum('costo_real'))['costo_real__sum'] or 0,
            'horas_totales_trabajadas': ordenes.aggregate(Sum('horas_trabajadas'))['horas_trabajadas__sum'] or 0,
        }
        
        serializer = EstadisticasEquipoSerializer(estadisticas)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_empresa(self, request):
        """Obtener equipos filtrados por empresa"""
        empresa_id = request.query_params.get('empresa', None)
        if empresa_id:
            equipos = self.queryset.filter(empresa_id=empresa_id)
            page = self.paginate_queryset(equipos)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(equipos, many=True)
            return Response(serializer.data)
        return Response({'error': 'empresa parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def operativos(self, request):
        """Obtener solo equipos operativos"""
        equipos = self.queryset.filter(estado='operativo', activo=True)
        page = self.paginate_queryset(equipos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(equipos, many=True)
        return Response(serializer.data)


class TecnicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Técnicos.
    
    Métodos disponibles:
    - GET /tecnicos/ - Listar todos los técnicos
    - POST /tecnicos/ - Crear nuevo técnico
    - GET /tecnicos/{id}/ - Obtener detalles del técnico
    - PUT /tecnicos/{id}/ - Actualizar técnico
    - DELETE /tecnicos/{id}/ - Eliminar técnico
    - GET /tecnicos/por-empresa/{empresa_id}/ - Técnicos de una empresa
    - GET /tecnicos/por-especialidad/{especialidad}/ - Técnicos por especialidad
    """
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'apellido', 'rut', 'email', 'especialidad']
    ordering_fields = ['apellido', 'experiencia_anos', 'fecha_contratacion']
    ordering = ['apellido']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TecnicoDetailSerializer
        return TecnicoSerializer

    @action(detail=False, methods=['get'])
    def por_empresa(self, request):
        """Obtener técnicos de una empresa específica"""
        empresa_id = request.query_params.get('empresa', None)
        if empresa_id:
            tecnicos = self.queryset.filter(empresas__id=empresa_id).distinct()
            page = self.paginate_queryset(tecnicos)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(tecnicos, many=True)
            return Response(serializer.data)
        return Response({'error': 'empresa parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def por_especialidad(self, request):
        """Obtener técnicos por especialidad"""
        especialidad = request.query_params.get('especialidad', None)
        if especialidad:
            tecnicos = self.queryset.filter(especialidad=especialidad, activo=True)
            page = self.paginate_queryset(tecnicos)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(tecnicos, many=True)
            return Response(serializer.data)
        return Response({'error': 'especialidad parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Obtener técnicos disponibles (activos)"""
        tecnicos = self.queryset.filter(activo=True)
        page = self.paginate_queryset(tecnicos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tecnicos, many=True)
        return Response(serializer.data)


class PlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Planes de Mantenimiento.
    
    Métodos disponibles:
    - GET /planes/ - Listar todos los planes
    - POST /planes/ - Crear nuevo plan
    - GET /planes/{id}/ - Obtener detalles del plan
    - PUT /planes/{id}/ - Actualizar plan
    - DELETE /planes/{id}/ - Eliminar plan
    - GET /planes/por-equipo/{equipo_id}/ - Planes de un equipo
    - GET /planes/activos/ - Solo planes activos
    """
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'tipo', 'frecuencia']
    ordering_fields = ['nombre', 'tipo', 'fecha_inicio']
    ordering = ['-fecha_creacion']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlanDetailSerializer
        return PlanSerializer

    @action(detail=False, methods=['get'])
    def por_equipo(self, request):
        """Obtener planes de un equipo específico"""
        equipo_id = request.query_params.get('equipo', None)
        if equipo_id:
            planes = self.queryset.filter(equipo_id=equipo_id)
            page = self.paginate_queryset(planes)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(planes, many=True)
            return Response(serializer.data)
        return Response({'error': 'equipo parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtener solo planes activos"""
        planes = self.queryset.filter(activo=True)
        page = self.paginate_queryset(planes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(planes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def proximos_vencimientos(self, request):
        """Obtener planes próximos a vencer (próximos 7 días)"""
        hoy = timezone.now().date()
        planes = self.queryset.filter(
            activo=True,
            fecha_proximo_mantenimiento__lte=hoy + timedelta(days=7),
            fecha_proximo_mantenimiento__gte=hoy
        )
        page = self.paginate_queryset(planes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(planes, many=True)
        return Response(serializer.data)


class OrdenViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Órdenes de Trabajo.
    
    Métodos disponibles:
    - GET /ordenes/ - Listar todas las órdenes
    - POST /ordenes/ - Crear nueva orden
    - GET /ordenes/{id}/ - Obtener detalles de la orden
    - PUT /ordenes/{id}/ - Actualizar orden
    - DELETE /ordenes/{id}/ - Eliminar orden
    - GET /ordenes/{id}/iniciar/ - Iniciar orden
    - GET /ordenes/{id}/completar/ - Completar orden
    - GET /ordenes/por-tecnico/{tecnico_id}/ - Órdenes por técnico
    - GET /ordenes/pendientes/ - Órdenes pendientes
    """
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero_orden', 'equipo__nombre', 'descripcion']
    ordering_fields = ['fecha_programada', 'prioridad', 'estado']
    ordering = ['-fecha_programada']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrdenDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return OrdenCrearActualizarSerializer
        return OrdenListSerializer if self.action == 'list' else OrdenSerializer

    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        """Iniciar la ejecución de una orden"""
        orden = self.get_object()
        
        if orden.estado != 'programada':
            return Response(
                {'error': 'Solo se pueden iniciar órdenes programadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orden.estado = 'en_progreso'
        orden.fecha_inicio = timezone.now()
        orden.save()
        
        serializer = OrdenSerializer(orden)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        """Completar una orden"""
        orden = self.get_object()
        
        if orden.estado == 'completada':
            return Response(
                {'error': 'La orden ya está completada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orden.estado = 'completada'
        orden.fecha_termino = timezone.now()
        
        # Calcular horas si no están ingresadas
        if not orden.horas_trabajadas and orden.fecha_inicio:
            horas = (orden.fecha_termino - orden.fecha_inicio).total_seconds() / 3600
            orden.horas_trabajadas = round(horas, 2)
        
        orden.save()
        
        serializer = OrdenSerializer(orden)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def pausar(self, request, pk=None):
        """Pausar una orden en progreso"""
        orden = self.get_object()
        
        if orden.estado != 'en_progreso':
            return Response(
                {'error': 'Solo se pueden pausar órdenes en progreso'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orden.estado = 'pausada'
        orden.save()
        
        serializer = OrdenSerializer(orden)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancelar una orden"""
        orden = self.get_object()
        
        if orden.estado == 'completada':
            return Response(
                {'error': 'No se puede cancelar una orden completada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orden.estado = 'cancelada'
        orden.save()
        
        serializer = OrdenSerializer(orden)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_tecnico(self, request):
        """Obtener órdenes asignadas a un técnico"""
        tecnico_id = request.query_params.get('tecnico', None)
        if tecnico_id:
            ordenes = self.queryset.filter(tecnico_asignado_id=tecnico_id)
            page = self.paginate_queryset(ordenes)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(ordenes, many=True)
            return Response(serializer.data)
        return Response({'error': 'tecnico parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Obtener órdenes pendientes (programadas o en progreso)"""
        ordenes = self.queryset.filter(estado__in=['programada', 'en_progreso', 'pausada'])
        page = self.paginate_queryset(ordenes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(ordenes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def urgentes(self, request):
        """Obtener órdenes urgentes pendientes"""
        ordenes = self.queryset.filter(
            prioridad='urgente',
            estado__in=['programada', 'en_progreso', 'pausada']
        )
        page = self.paginate_queryset(ordenes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(ordenes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Obtener órdenes vencidas (programadas para fecha pasada)"""
        ordenes = self.queryset.filter(
            fecha_programada__lt=timezone.now(),
            estado__in=['programada', 'pendiente']
        )
        page = self.paginate_queryset(ordenes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(ordenes, many=True)
        return Response(serializer.data)


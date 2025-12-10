from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet, EquipoViewSet, TecnicoViewSet,
    PlanViewSet, OrdenViewSet
)

# Crear router y registrar ViewSets
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'equipos', EquipoViewSet, basename='equipo')
router.register(r'tecnicos', TecnicoViewSet, basename='tecnico')
router.register(r'planes', PlanViewSet, basename='plan')
router.register(r'ordenes', OrdenViewSet, basename='orden')

app_name = 'mantenimiento'

urlpatterns = [
    path('', include(router.urls)),
]

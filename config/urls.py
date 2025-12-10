"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """Root endpoint de la API"""
    return Response({
        'message': 'Mantención Industrial API',
        'version': '1.0.0',
        'endpoints': {
            'empresas': request.build_absolute_uri('/api/empresas/'),
            'equipos': request.build_absolute_uri('/api/equipos/'),
            'tecnicos': request.build_absolute_uri('/api/tecnicos/'),
            'planes': request.build_absolute_uri('/api/planes/'),
            'ordenes': request.build_absolute_uri('/api/ordenes/'),
            'admin': request.build_absolute_uri('/admin/'),
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('mantenimiento.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

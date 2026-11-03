from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from zeep import Client
from zeep.exceptions import Error as ZeepError
from zeep.helpers import serialize_object

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import obtener_estrategia

COUNTRY_INFO_WSDL = (
    'http://webservices.oorsprong.org/websamples.countryinfo/'
    'CountryInfoService.wso?WSDL'
)
_country_info_client = None


def _get_country_info_client():
    global _country_info_client
    if _country_info_client is None:
        _country_info_client = Client(COUNTRY_INFO_WSDL)
    return _country_info_client


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def precio_final(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    estrategia = obtener_estrategia(producto.category.name)
    precio_con_descuento = estrategia.calcular(float(producto.price))

    return Response({
        'producto': producto.name,
        'precio_original': producto.price,
        'precio_final': round(precio_con_descuento, 2),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pais_info(request):
    iso_code = request.query_params.get('iso', 'MX').upper()
    try:
        client = _get_country_info_client()
        resultado = client.service.FullCountryInfo(sCountryISOCode=iso_code)
    except ZeepError:
        return Response(
            {'error': 'No se pudo consultar el servicio SOAP de países.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response(serialize_object(resultado, target_cls=dict))


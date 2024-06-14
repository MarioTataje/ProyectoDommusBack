from rest_framework.decorators import api_view
from rest_framework.views import *
from .serializers import RegionSerializer, ProvinceSerializer, DistrictSerializer
from .models import Region, Province, District


@api_view(['GET'])
def regions_list(request):
    if request.method == 'GET':
        try:
            regions = Region.objects.all()
            serializer = RegionSerializer(regions, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)

@api_view(['GET'])
def list_provinces_by_region(request, region_id):
    if request.method == 'GET':
        provinces = Province.objects.filter(region_id=region_id)
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def list_districts_by_province(request, province_id):
    if request.method == 'GET':
        districts = District.objects.filter(province_id=province_id)
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)
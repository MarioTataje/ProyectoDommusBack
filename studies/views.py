from rest_framework.decorators import api_view
from rest_framework.views import *
from .serializers import UniversitySerializer, DegreeSerializer
from .models import University, Degree


@api_view(['GET'])
def universities_list(request):
    if request.method == 'GET':
        universities = University.objects.all()
        serializer = UniversitySerializer(universities, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def degrees_list(request, university_id):
    try:
        University.objects.get(id=university_id)
    except University.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        degrees = Degree.objects.filter(universities__id=university_id)
        serializer = DegreeSerializer(degrees, many=True)
        return Response(serializer.data)



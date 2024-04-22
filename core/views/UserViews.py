from core.serializers import UsuarioSerializer
from core.models import Usuario
from core.models import Carrera
from core.models import Universidad
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class UsuarioList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        newCarrera = Carrera.objects.get(pk=request.data['carrera'])
        newUniversidad = Universidad.objects.get(pk=newCarrera.universidad.idUniversidad)
        if newUniversidad.extension != [i for i in request.data['correo'].split('@')][1]:
            return Response({'correo': 'El correo ingresado no corresponde a la universidad seleccionada.'}, status=status.HTTP_400_BAD_REQUEST)

        request.data._mutable = True
        request.data['usuarioAdicion'] = request.data.pop('usuario')[0]

        return self.create(request, *args, **kwargs)


class UsuarioDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['usuarioModificacion'] = request.data.pop('usuario')[0]
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

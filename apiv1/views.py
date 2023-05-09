from rest_framework.viewsets import ModelViewSet

from apiv1.serializers import MaterialSerializer
from cost import models


class MaterialViewSet(ModelViewSet):
    queryset = models.Material.objects.all()
    serializer_class = MaterialSerializer

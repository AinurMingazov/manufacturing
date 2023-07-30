from rest_framework import serializers

from cost import models


class MaterialSerializer(serializers.ModelSerializer):
    """Вывод материал"""

    class Meta:
        model = models.Material
        fields = "__all__"

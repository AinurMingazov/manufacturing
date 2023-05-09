from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apiv1 import serializers
from cost import models


class MaterialApiTestCase(APITestCase):
    def test_get(self):
        material_1 = models.Material.objects.create(
            name="Круг 100мм сталь 35 ГОСТ 1050-2013",
            price_per_meter="100.00",
            price_per_ton="73500.00",
        )
        material_2 = models.Material.objects.create(
            name="Круг 105мм сталь 40Х ГОСТ 4543-71",
            price_per_meter="105.00",
            price_per_ton="77500.00",
        )
        url = reverse("material-list")
        response = self.client.get(url)
        serializer_data = serializers.MaterialSerializer(
            [material_1, material_2], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

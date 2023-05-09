from django.test import TestCase

from apiv1 import serializers
from cost import models


class MaterialSerializerTestCase(TestCase):
    def test_ok(self):
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
        data = serializers.MaterialSerializer([material_1, material_2], many=True).data
        expected_data = [
            {
                "id": material_1.id,
                "name": "Круг 100мм сталь 35 ГОСТ 1050-2013",
                "unit": "кг",
                "price_per_meter": "100.00",
                "price_per_ton": "73500.00",
            },
            {
                "id": material_2.id,
                "name": "Круг 105мм сталь 40Х ГОСТ 4543-71",
                "unit": "кг",
                "price_per_meter": "105.00",
                "price_per_ton": "77500.00",
            },
        ]
        self.assertEqual(data, expected_data)

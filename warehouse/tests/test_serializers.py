from django.test import TestCase
from warehouse.serializers import PaintSerializer
from warehouse.models import Paint, Serie, Manufacturer


class PaintSerializerTestCase(TestCase):
    def test_ok(self):
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer 1')
        serie = Serie.objects.create(name='Test Serie 1', manufacturer=manufacturer)
        paint_1 = Paint.objects.create(
            name='Test 1', manufacturer=manufacturer, series=serie
        )
        paint_2 = Paint.objects.create(
            name='Test 2', manufacturer=manufacturer, series=serie
        )
        data = PaintSerializer([paint_1, paint_2], many=True).data

        expected_data = [
            {'id': paint_1.id, 'name': 'Test 1'},
        ]
        self.assertEqual(expected_data, data)

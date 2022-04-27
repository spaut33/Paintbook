from django.test import TestCase
from warehouse.serializers import PaintSerializer
from warehouse.models import Paint, Series, Manufacturer


class PaintSerializerTestCase(TestCase):
    def test_ok(self):
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer 1')
        series = Series.objects.create(name='Test Series 1', manufacturer=manufacturer)
        paint_1 = Paint.objects.create(
            name='Test 1', manufacturer=manufacturer, series=series
        )
        paint_2 = Paint.objects.create(
            name='Test 2', manufacturer=manufacturer, series=series
        )
        data = PaintSerializer(paint_1).data

        expected_data = {'id': paint_1.id, 'name': 'Test 1', 'quantity': 1}

        self.assertEqual(expected_data, data)

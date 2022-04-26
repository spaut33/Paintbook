from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from warehouse.models import Paint, Serie, Manufacturer
from warehouse.serializers import PaintSerializer


class PaintsApiTestCase(APITestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer 1')
        serie = Serie.objects.create(name='Test Serie 1', manufacturer=manufacturer)
        self.paint_1 = Paint.objects.create(
            name='Test 1',
            article='600.00.00',
            manufacturer=manufacturer,
            series=serie,
            quantity=1,
        )
        self.paint_2 = Paint.objects.create(
            name='Test 2',
            article='700.00.00',
            manufacturer=manufacturer,
            series=serie,
            quantity=5,
        )
        self.paint_3 = Paint.objects.create(
            name='Test 3 600.00.00',
            article='100.00.00',
            manufacturer=manufacturer,
            series=serie,
            quantity=1,
        )

    def test_get(self):
        url = reverse('paint-list')

        # url = 'http://127.0.0.1/paints/?format=json'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            PaintSerializer([self.paint_1, self.paint_2, self.paint_3], many=True).data,
            response.data,
        )

    def test_get_filter(self):
        url = reverse('paint-list')

        # url = 'http://127.0.0.1/paints/?format=json'
        response = self.client.get(url, data={'quantity': '5'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            PaintSerializer([self.paint_2], many=True).data,
            response.data,
        )

    def test_get_search(self):
        url = reverse('paint-list')

        # url = 'http://127.0.0.1/paints/?format=json'
        response = self.client.get(url, data={'search': '600.00.00'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            PaintSerializer([self.paint_1, self.paint_3], many=True).data,
            response.data,
        )

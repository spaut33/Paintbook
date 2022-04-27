import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from warehouse.models import Paint, Series, Manufacturer
from warehouse.serializers import PaintSerializer


class PaintsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer 1')
        series = Series.objects.create(name='Test Series 1', manufacturer=manufacturer)
        self.paint_1 = Paint.objects.create(
            name='Test 1',
            article='600.00.00',
            manufacturer=manufacturer,
            series=series,
            quantity=1,
        )
        self.paint_2 = Paint.objects.create(
            name='Test 2',
            article='700.00.00',
            manufacturer=manufacturer,
            series=series,
            quantity=5,
        )
        self.paint_3 = Paint.objects.create(
            name='Test 3 600.00.00',
            article='100.00.00',
            manufacturer=manufacturer,
            series=series,
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

    # CRUD Tests
    def test_create(self):
        url = reverse('paint-list')
        data = {
            'name': 'Test name CRUD',
            'article': '555.CRUD.Test',
            'series': 1,
            'manufacturer': 1,
            'quantity': 500
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

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
        # 3 items were created during setup
        self.assertEqual(3, Paint.objects.all().count())
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # 4th item created
        self.assertEqual(4, Paint.objects.all().count())

    def test_update(self):
        url = reverse('paint-detail', args=(self.paint_1.id,))
        data = {
            'name': 'Changed name CRUD',
            'quantity': 5,
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.paint_1.refresh_from_db()
        self.assertEqual(5, self.paint_1.quantity)

    def test_delete(self):
        url = reverse('paint-detail', args=(self.paint_3.id,))
        self.assertEqual(3, Paint.objects.all().count())
        # json_data = json.dumps(data)

        self.client.force_login(self.user)
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Paint.objects.all().count())


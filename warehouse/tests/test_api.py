import json

from django.db.models import Avg, Max
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from warehouse.models import Paint, Series, Manufacturer, UserPaint
from warehouse.serializers import PaintSerializer


class PaintsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user_staff = User.objects.create(username='admin_user', is_staff=True)
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer 1')
        series = Series.objects.create(name='Test Series 1', manufacturer=manufacturer)
        self.paint_1 = Paint.objects.create(
            name='Test 1',
            catalog_number='600.00.00',
            manufacturer=manufacturer,
            series=series,
            owner=self.user,
        )
        self.paint_2 = Paint.objects.create(
            name='Test 2',
            catalog_number='700.00.00',
            manufacturer=manufacturer,
            series=series,
            published=False,
        )
        self.paint_3 = Paint.objects.create(
            name='Test 3 600.00.00',
            catalog_number='100.00.00',
            manufacturer=manufacturer,
            series=series,
            owner=self.user,
        )

    def test_get_list(self):
        url = reverse('paint-list')

        response = self.client.get(url)
        paints = Paint.objects.all().annotate(average_rating=Avg('userpaint__rating'),
                                              max_rating=Max('userpaint__rating'))
        serializer_data = PaintSerializer(paints, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            serializer_data,
            response.data
        )
        self.assertEqual(serializer_data[0]['average_rating'], None)
        self.assertEqual(serializer_data[0]['max_rating'], None)

    def test_get_filter(self):
        url = reverse('paint-list')
        paints = Paint.objects.filter(id=self.paint_2.id).annotate(average_rating=Avg('userpaint__rating'),
                                                                   max_rating=Max('userpaint__rating')).order_by('id')
        response = self.client.get(url, data={'published': 0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            PaintSerializer(paints, many=True).data,
            response.data,
        )

    def test_get_search(self):
        url = reverse('paint-list')
        paints = Paint.objects.filter(id__in=[self.paint_1.id, self.paint_3.id]).annotate(
            average_rating=Avg('userpaint__rating'),
            max_rating=Max('userpaint__rating'))
        response = self.client.get(url, data={'search': '600.00.00'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            PaintSerializer(paints, many=True).data,
            response.data
        )

    # CRUD Tests
    def test_create(self):
        url = reverse('paint-list')
        data = {
            'name': 'Test name CRUD',
            'article': '555.CRUD.Test',
            'series': 1,
            'manufacturer': 1,
        }
        json_data = json.dumps(data)
        # 3 items were created during setup
        self.assertEqual(3, Paint.objects.all().count())
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # 4th item created
        self.assertEqual(4, Paint.objects.all().count())
        self.assertEqual(self.user, Paint.objects.last().owner)

    def test_update(self):
        url = reverse('paint-detail', args=(self.paint_1.id,))
        data = {
            'name': 'Changed name CRUD',
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.paint_1.refresh_from_db()
        self.assertEqual('Changed name CRUD', self.paint_1.name)

    def test_delete(self):
        url = reverse('paint-detail', args=(self.paint_3.id,))
        self.assertEqual(3, Paint.objects.all().count())

        self.client.force_login(self.user)
        response = self.client.delete(url, content_type='application/json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Paint.objects.all().count())

    def test_update_not_owner(self):
        # Test for updating the paint if user is not the owner of this paint
        # Test returns 403 error, and it's ok because not owner shouldn't change the paint
        self.user2 = User.objects.create(username='test_username_2')
        url = reverse('paint-detail', args=(self.paint_1.id,))
        data = {
            'name': 'Changed name CRUD',
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        print(response.data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.paint_1.refresh_from_db()
        self.assertEqual('Test 1', self.paint_1.name)

    def test_update_not_owner_but_staff(self):
        # Test for updating the paint if user is not the owner of this paint
        url = reverse('paint-detail', args=(self.paint_1.id,))
        data = {
            'name': 'Changed name CRUD',
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user_staff)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.paint_1.refresh_from_db()
        self.assertEqual('Changed name CRUD', self.paint_1.name)

    def test_delete_not_owner(self):
        # Test for deleting the paint if user is not the owner of this paint
        # Test returns 403 error, and it's ok because not owner shouldn't delete the paint
        self.user2 = User.objects.create(username='test_username_2')
        url = reverse('paint-detail', args=(self.paint_3.id,))
        self.assertEqual(3, Paint.objects.all().count())

        self.client.force_login(self.user2)
        response = self.client.delete(url, content_type='application/json')
        print(response.data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Paint.objects.all().count())

    def test_delete_not_owner_but_staff(self):
        # Test for deleting the paint if user is not the owner but has is_staff flag
        url = reverse('paint-detail', args=(self.paint_3.id,))
        self.assertEqual(3, Paint.objects.all().count())

        self.client.force_login(self.user_staff)
        response = self.client.delete(url, content_type='application/json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Paint.objects.all().count())


class UserPaintsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user_staff = User.objects.create(username='admin_user', is_staff=True)
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer 1')
        series = Series.objects.create(name='Test Series 1', manufacturer=manufacturer)
        self.paint_1 = Paint.objects.create(
            name='Test 1',
            catalog_number='600.00.00',
            manufacturer=manufacturer,
            series=series,
            owner=self.user,
        )
        self.paint_2 = Paint.objects.create(
            name='Test 2',
            catalog_number='700.00.00',
            manufacturer=manufacturer,
            series=series,
            published=False,
        )
        self.paint_3 = Paint.objects.create(
            name='Test 3 600.00.00',
            catalog_number='100.00.00',
            manufacturer=manufacturer,
            series=series,
            owner=self.user,
        )

    def test_favorite(self):
        # Tests if user added paint to a list of favorites paints
        url = reverse('userpaint-detail', args=(self.paint_1.id,))

        data = {
            'favorite': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_paint = UserPaint.objects.get(user=self.user, paint=self.paint_1)
        self.assertTrue(user_paint.favorite)

    def test_rating(self):
        # Tests if user added paint to a list of favorites paints
        url = reverse('userpaint-detail', args=(self.paint_1.id,))

        data = {
            'rating': 4,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_paint = UserPaint.objects.get(user=self.user, paint=self.paint_1)
        self.assertEqual(4, user_paint.rating)

        # Test against wrong rating numbers (we have to accept 1-5 only)
        data = {
            'rating': 1000,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'rating': 'test',
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'rating': -400,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'rating': 0,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

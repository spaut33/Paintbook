from django.contrib.auth.models import User
from django.db.models import Avg, Max
from django.test import TestCase
from warehouse.serializers import PaintSerializer
from warehouse.models import Paint, Series, Manufacturer, UserPaint


class PaintSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='User1')
        user2 = User.objects.create(username='User2')
        user3 = User.objects.create(username='User3')
        manufacturer = Manufacturer.objects.create(name='Test Manufacturer 1')
        series = Series.objects.create(name='Test Series 1', manufacturer=manufacturer)
        paint_1 = Paint.objects.create(
            name='Test 1', manufacturer=manufacturer, series=series
        )
        paint_2 = Paint.objects.create(
            name='Test 2', manufacturer=manufacturer, series=series
        )

        UserPaint.objects.create(user=user1, paint=paint_1, rating=2)
        UserPaint.objects.create(user=user2, paint=paint_1, rating=3)
        UserPaint.objects.create(user=user3, paint=paint_1, rating=4)
        UserPaint.objects.create(user=user1, paint=paint_2, rating=1)

        paints = Paint.objects.all().annotate(average_rating=Avg('userpaint__rating'), max_rating=Max('userpaint__rating')).order_by('id')
        data = PaintSerializer(paints, many=True).data
        print(data)
        expected_data = [
            {
                'id': paint_1.id,
                'name': 'Test 1',
                'average_rating': 3.0,
                'max_rating': 4.0,
            },
            {
                'id': paint_2.id,
                'name': 'Test 2',
                'average_rating': 1,
                'max_rating': 1,
            },
        ]
        self.assertEqual(expected_data, data)

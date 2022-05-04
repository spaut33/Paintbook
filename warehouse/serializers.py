from django.db.models import Avg, Max
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from warehouse.models import Paint, UserPaint


class PaintSerializer(ModelSerializer):

    average_rating = serializers.DecimalField(max_digits=2, decimal_places=1, read_only=True)
    max_rating = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)

    class Meta:
        model = Paint
        fields = ('id', 'name', 'average_rating', 'max_rating', 'owner_name')


class UserPaintSerializer(ModelSerializer):
    class Meta:
        model = UserPaint
        fields = ('paint', 'favorite', 'rating', 'quantity')

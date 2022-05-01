from rest_framework.serializers import ModelSerializer

from warehouse.models import Paint, UserPaint


class PaintSerializer(ModelSerializer):
    class Meta:
        model = Paint
        fields = '__all__'


class UserPaintSerializer(ModelSerializer):
    class Meta:
        model = UserPaint
        fields = ('paint', 'favorite', 'rating', 'quantity')

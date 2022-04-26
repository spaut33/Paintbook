from rest_framework.serializers import ModelSerializer

from warehouse.models import Paint


class PaintSerializer(ModelSerializer):
    class Meta:
        model = Paint
        fields = ('id', 'name')

from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render

from warehouse.models import Paint, UserPaint
from warehouse.permissions import IsOwnerOrAdminOrReadOnly
from warehouse.serializers import PaintSerializer, UserPaintSerializer


def auth(request):
    return render(request, 'oauth.html')


# Create your views here.
class PaintsViewSet(ModelViewSet):
    queryset = Paint.objects.all()
    serializer_class = PaintSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filter_fields = ['manufacturer', 'published']
    search_fields = ['name', 'catalog_number', 'description']
    ordering_fields = ['time_added', 'color']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserPaintViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPaint.objects.all()
    serializer_class = UserPaintSerializer
    lookup_field = 'paint'

    def get_object(self):
        obj, _ = UserPaint.objects.get_or_create(user=self.request.user, paint_id=self.kwargs['paint'])
        return obj

from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render

from warehouse.models import Paint
from warehouse.permissions import IsOwnerOrAdminOrReadOnly
from warehouse.serializers import PaintSerializer


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


def auth(request):
    return render(request, 'oauth.html')

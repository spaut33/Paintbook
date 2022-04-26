from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render

from warehouse.models import Paint
from warehouse.serializers import PaintSerializer


# Create your views here.
class PaintsViewSet(ModelViewSet):
    queryset = Paint.objects.all()
    serializer_class = PaintSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    filter_fields = ['quantity']
    search_fields = ['name', 'article', 'description']
    ordering_fields = ['quantity', 'color']


def auth(request):
    return render(request, 'oauth.html')

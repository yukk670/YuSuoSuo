from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from rest_framework.decorators import action
from .models import Video
from .serializers import VideoSerializer,VideoDetailSerializer

class VideoViewSet(viewsets.ModelViewSet):
    class PaginationClass(CursorPagination):
        page_size = 5
        ordering = '-putaway_time'

    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    pagination_class = PaginationClass


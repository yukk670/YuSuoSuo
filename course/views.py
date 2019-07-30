from rest_framework import status,viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination

from course.models import ProblemSet,Course
# Create your views here.
from course.serializers import *

class CourseViewSet(viewsets.GenericViewSet):
    class PaginationClass(CursorPagination):
        page_size = 4
        ordering = '-putaway_time'

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = PaginationClass

    @action(detail=0)
    def c_list(self,request):
        pagination = self.pagination_class()
        pagination_list = pagination.paginate_queryset(self.queryset,request,self)
        data = self.serializer_class(pagination_list,many=True).data
        return pagination.get_paginated_response(data)

    @action(detail=0,url_path="c_detail/(?P<c_id>\S+)")
    def c_detail(self,request,c_id,*args,**kwargs):
        try:
            course = Course.objects.get(id=c_id.strip())

            data = CourseDetailSerializer(course).data
        except Exception as e:
            return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data)

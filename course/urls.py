from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'course'

router = DefaultRouter()
router.register('',views.CourseViewSet)

urlpatterns = [
    path('',include(router.urls)),
]

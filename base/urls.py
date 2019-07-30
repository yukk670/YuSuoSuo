from django.urls import include,path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'base'

router = DefaultRouter()
router.register(r'videos',views.VideoViewSet)

urlpatterns = [
    path('',include(router.urls)),
]

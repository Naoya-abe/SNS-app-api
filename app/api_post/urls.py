from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_post import views

app_name = 'post'

router = DefaultRouter()
router.register('', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]

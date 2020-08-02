from django.urls import path, include
from rest_framework.routes import DefaultRouter
from api_post import views

app_name = 'post'

router = DefaultRouter()
router.register('post', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls))
]

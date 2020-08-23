from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_post import views

app_name = 'post'

router = DefaultRouter()
router.register('', views.PostViewSet)

urlpatterns = [
    path('myposts/', views.MyPostListView.as_view(), name='myposts'),
    path('friend-posts/', views.FriendPostListView.as_view(), name='friend-posts'),
    path('', include(router.urls))
]

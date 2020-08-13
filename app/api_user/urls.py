from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_user import views

app_name = 'user'

router = DefaultRouter()
router.register('profiles', views.UserViewSet)
router.register('approval', views.FriendRequestViewSet)

urlpatterns = [
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('', include(router.urls))
]

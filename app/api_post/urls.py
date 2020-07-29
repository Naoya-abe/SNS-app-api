from django.urls import path,include
from rest_framework.routes import DefaultRouter

app_name='post'

router=DefaultRouter()

urlpatterns=[
    path('',include(router.urls))
]
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('blog', BlogViewSet, basename='blog') # (게시글)
router.register('comment', CommentViewSet, basename='comment') # (댓글)

urlpatterns =[
    path('', include(router.urls))
]
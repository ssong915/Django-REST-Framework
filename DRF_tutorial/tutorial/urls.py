from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('', include('snippets.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
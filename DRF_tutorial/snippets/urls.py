from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers

# # urlpatterns = [
# #     ## 함수기반
# #     # path('snippets/', views.snippet_list),
# #     # path('snippets/<int:pk>', views.snippet_detail),

# #     ## 클래스기반 
# #     path('snippets/', views.SnippetList.as_view()),
# #     path('snippets/<int:pk>/', views.SnippetDetail.as_view()),

# #     path('users/', views.UserList.as_view()),
# #     path('users/<int:pk>/', views.UserDetail.as_view()),

# #     path('', views.api_root),
# #     path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
# # ]

# # API endpoints
# urlpatterns = format_suffix_patterns([
#     path('', views.api_root),
#     path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
#     path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
#     path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
#     path('users/', views.UserList.as_view(), name='user-list'),
#     path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail')
# ])



# urlpatterns = format_suffix_patterns(urlpatterns)

snippet_list = SnippetViewSet.as_view({
    'get': 'list',    # 메소드에 따라 필요한 액션들을 바인딩 한다.
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])

 ### 1. 함수기반 View

 # from django.http import HttpResponse, JsonResponse
 # from django.views.decorators.csrf import csrf_exempt
 # from rest_framework.parsers import JSONParser
 # from snippets.models import Snippet
 # from snippets.serializers import SnippetSerialize

 # #Read,Creat
 # @csrf_exempt
 # def snippet_list(request):
 #     """
 #     List all code snippets, or create a new snippet.
 #     """
 #     if request.method == 'GET':
 #         snippets = Snippet.objects.all()
 #         serializer = SnippetSerializer(snippets, many=True)
 #         return JsonResponse(serializer.data, safe=False
 #     elif request.method == 'POST':
 #         data = JSONParser().parse(request) # 역직렬화: 문자열 -> 객체
 #         serializer = SnippetSerializer(data=data)
 #         if serializer.is_valid():
 #             serializer.save()
 #             return JsonResponse(serializer.data, status=201)
 #         return JsonResponse(serializer.errors, status=400
 
 # # Read, Upate,Delet
 # @csrf_exempt
 # def snippet_detail(request, pk):
 #     """
 #     Retrieve, update or delete a code snippet.
 #     """
 #     try:
 #         snippet = Snippet.objects.get(pk=pk)
 #     except Snippet.DoesNotExist:
 #         return HttpResponse(status=404
 #     if request.method == 'GET':
 #         serializer = SnippetSerializer(snippet)
 #         return JsonResponse(serializer.data
 #     elif request.method == 'PUT':
 #         data = JSONParser().parse(request)
 #         serializer = SnippetSerializer(snippet, data=data)
 #         if serializer.is_valid():
 #             serializer.save()
 #             return JsonResponse(serializer.data)
 #         return JsonResponse(serializer.errors, status=400
 #     elif request.method == 'DELETE':
 #         snippet.delete()
 #         return HttpResponse(status=204)



### 2. 함수기반 View -api_view 데코레이터를 이용한 리팩토링ver

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer


# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


### 3. 클래스기반 View

# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status


# class SnippetList(APIView):
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


### 4.클래스기반View -mixin 클래스 활용하여 리팩토링

# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import mixins
# from rest_framework import generics

# class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


### 5.클래스기반View -mixed-in generic 클래스 이용

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

from rest_framework import permissions
 # 접근권한을 위한 permission클래스들!
 # 로그인 유저만 생성,수정,삭제할 수 잇게 해보장 
 # 사용법: 먼저 사용하고자 하는 Permission 클래스를 import 하고,
 # 해당 접근 권한을 설정할 뷰의 permission_classes 변수에 그 Permission 클래스를 명시해주면 된다.
from snippets.permissions import IsOwnerOrReadOnly
 # 만들어둔 넘 갖다 쓰기
# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     # 인증이 이뤄진(= 로그인한 상태의) 요청들: 읽기 및 쓰기 권한을 가지도록 하고, 
#     # 인증이 이뤄지지 않은(= 로그인하지 않은 상태의) 요청: 읽기 권한만


#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user) 
#         # Snippet 인스턴스를 생성할 때 request 객체로 넘어오는 User 인스턴스가 연결
#         # User가 request 객체에 담겨옴
#         #serializer.save할때 user정보도 넘겨줄 수 있음
    


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

from rest_framework import renderers
from rest_framework.response import Response

# # 기본 클래스를 사용한다.
# # 객체 인스턴스(Snippet)를 반환하는 것이 아니라, 
# # 객체 인스턴스의 속성 중 하나(Snippet.highlighted)를 반환해야 하기 때문이다. 
# # concrete generic view를 사용하는 대신, 기본 클래스를 사용하고 자체 .get() 함수를 만들어 보자. 
# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]

#     # 자체 get() 함수를 구현한다.
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
        
#         # Snippet.highlighted를 반환한다.
#         return Response(snippet.highlighted)

# 6강 ViewSet을 이용한 리팩토링: SnippetList & SnippetDetail & SnippetHighlight -> SnippetViewSet 

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets

#                    read/write 모든 작업을 제공한다.
class SnippetViewSet(viewsets.ModelViewSet): # ModelViewSet: read,write 지원
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

	# @action: 기존 SnippetHighlight 뷰를 위해 별도 함수를 추가한다. 
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

	# 이전과 마찬가지로, user와 이어주기 위해 perform_create를 오버라이드한다.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
#----------------------------------------------------------------------

# from django.contrib.auth.models import User
# from snippets.serializers import UserSerializer

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
# 6강 ViewSet을 이용한 리팩토링: UserList & UserDetail -> UserViewSet 
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import viewsets

# viewsets: drf에 포함된 추상클래스
# get과 put 함수를 지원하지 않고, 대신 read와 update 함수를 지원
class UserViewSet(viewsets.ReadOnlyModelViewSet): #Read only를 위해 ReadOnlyModelViewSet 클래스 추가
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


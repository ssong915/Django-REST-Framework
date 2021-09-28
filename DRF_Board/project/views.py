# 데이터 처리
from .models import Blog
from .serializers import BlogSerializer

# mixins 사용하기 위해 import
from rest_framework import generics
from rest_framework import mixins

# Blog의 목록을 보여주는 역할
class BlogList(mixins.ListModelMixin, 
                  mixins.CreateModelMixin, 
                  generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class =BlogSerializer

	# Blog list를 보여줄 때
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
	
	# 새로운 Blog 글을 작성할 때
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Blog의 detail을 보여주는 역할
class BlogDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

	# Blog의 detail 보기
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

	# Blog 수정하기
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

	# Blog 삭제하기
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
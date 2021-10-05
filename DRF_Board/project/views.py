from .models import Blog
from .serializers import BlogSerializer
from rest_framework import viewsets

# Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
   
   	# serializer.save() 재정의
    # 로그인되어있는 넘 작성자로 !!
    def perform_create(self, serializer):
        Blog.update_counter
        serializer.save(user = self.request.user)
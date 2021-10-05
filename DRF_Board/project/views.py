from .models import Blog
from .serializers import BlogSerializer
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class BlogViewSet(viewsets.ModelViewSet):
    # authentication 추가
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    # permission 추가 
    # IsAuthenticatedOrReadOnly : 비회원은 글을 볼 수만 있어야 하기 때문!
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
   
   	# serializer.save() 재정의
    # 로그인되어있는 넘 작성자로 !!
    def perform_create(self, serializer):
        Blog.update_counter
        serializer.save(user = self.request.user)
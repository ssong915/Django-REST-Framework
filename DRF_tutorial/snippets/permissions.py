# 특정 Snippet 인스턴스의 수정 및 삭제는 
# 그것을 생성한 유저만 가능하도록 접근 권한을 설정해보기
# permissions 에 내장된 기능이 아니므로 permissions.py 따로 만들어서 관리

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
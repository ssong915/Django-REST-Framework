from rest_framework import permissions

    ############ custom permission ############

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # GET, HEAD, OPTIONS 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # PUT, PATCH, DELETE
        # 객체(Blog)의 user ==  요청자(request.user) 인가?
        return obj.user == request.user
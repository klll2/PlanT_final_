# from rest_framework.permissions import BasePermission

# class IsAuthenticatedAndNotAdmin(BasePermission):
#     """
#     사용자 인증을 확인하지만 관리자인 경우 False를 반환하여 접근을 차단합니다.
#     """
#     def has_permission(self, request, view):
#         # 관리자인 경우 False를 반환하여 접근을 차단합니다.
#         if request.user and request.user.is_staff:
#             return False
#         # 관리자가 아닌 경우 인증 여부를 확인합니다.
#         return request.user and request.user.is_authenticated
    

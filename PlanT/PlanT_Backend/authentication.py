# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.tokens import UntypedToken
# from django.conf import settings
# from django.contrib.auth.models import User
# from rest_framework.exceptions import AuthenticationFailed
# import jwt

# class CustomJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         header = self.get_header(request)
#         if header is None:
#             return None

#         raw_token = self.get_raw_token(header)
#         if raw_token is None:
#             return None

#         validated_token = self.get_validated_token(raw_token)

#         try:
#             decoded_token = jwt.decode(validated_token, settings.SECRET_KEY, algorithms=['HS256'])
#             user_email = decoded_token.get('user_email')
#             if user_email is None:
#                 raise AuthenticationFailed("User email not found in token")

#             user = User.objects.get(user_email=user_email)
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Token has expired")
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed("Invalid token")
#         except User.DoesNotExist:
#             raise AuthenticationFailed("User not found")

#         return (user, validated_token)

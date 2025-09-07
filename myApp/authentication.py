from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from app.models import CustomUser
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise NotAuthenticated("Authorization header missing")

        try:
            token = auth_header.split(" ")[1]
            payload = AccessToken(token).payload

            user_id = payload.get(settings.SIMPLE_JWT["USER_ID_CLAIM"])
            if not user_id:
                raise AuthenticationFailed("Invalid auth token")

            user = self.get_user_by_id(user_id)
            if not user:
                raise AuthenticationFailed("Invalid auth token")

            return user, None

        except AuthenticationFailed as e:
            raise e
        except Exception as e:
            raise AuthenticationFailed("Invalid auth token")

    def get_user_by_id(self, user_id):
        raise NotImplementedError("Subclasses must implement this method")


class UserAuthentication(JWTAuthentication):
    def get_user_by_id(self, user_id):
        return CustomUser.objects.filter(id=user_id).first()
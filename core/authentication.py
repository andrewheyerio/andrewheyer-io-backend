# The authentication custom class manages the JWT token generation & authentication
import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from andrewheyer_io import settings
from core.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise exceptions.AuthenticationFailed('Authentication token was not found!')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Unable to decode authentication token")
        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        return (user, None)

    @staticmethod
    def generate_jwt(id):
        payload = {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

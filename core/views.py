from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from core.serializer import UserSerializer
from core.models import User
from .authentication import JWTAuthentication


# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password do not match!')

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']
        user = User.objects.filter(email=email).first()

        # If the user object with the given email is not found
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        # Because the user model inherits from BaseUserModel we can call super method check_password
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect password")

        # No exceptions by this point, success!
        token = JWTAuthentication.generate_jwt(user.id)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'success'
        }
        return response


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, __):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'success'
        }
        return response

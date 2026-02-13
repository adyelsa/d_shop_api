from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer, ConfirmSerializer
from .models import UserConfirmation


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserConfirmation.objects.create(user=user)
            return Response({"message": "User created. Confirm your account."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )

            if user is None:
                return Response({"error": "Invalid credentials"}, status=400)

            if not user.is_active:
                return Response({"error": "User is not confirmed"}, status=403)

            return Response({"message": "Login success"})

        return Response(serializer.errors, status=400)



class ConfirmView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            code = serializer.validated_data["code"]

            try:
                user = User.objects.get(username=username)
                confirmation = UserConfirmation.objects.get(user=user)
            except:
                return Response({"error": "User not found"}, status=404)

            if confirmation.code != code:
                return Response({"error": "Invalid code"}, status=400)

            user.is_active = True
            user.save()

            confirmation.is_confirmed = True
            confirmation.save()

            return Response({"message": "User confirmed"})

        return Response(serializer.errors, status=400)
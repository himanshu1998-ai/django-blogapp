from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status


class RegisterView(APIView):
    
    def post(self, request):
        try:
            serialzer = RegisterSerializer(data= request.data)
            if not serialzer.is_valid():
                return Response({"data": serialzer.errors,"message": "something went wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
            serialzer.save()
            return Response({"data": {}, "message": "Your account is created"},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            
            return Response({"data": {}, "message": "something went wrong"},
                                status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    
    def post(self, request):
        try:
            serialzer = LoginSerializer(data= request.data)
            if not serialzer.is_valid():
                return Response({"data": serialzer.errors,"message": "something went wrong"},
                                status=status.HTTP_400_BAD_REQUEST)
            token_data = serialzer.get_jwt_token(serialzer.data)
            return Response(token_data,
                                status=status.HTTP_200_OK)
        except Exception as e:

            return Response({"data": str(e), "message": "something went wrong"},
                                status=status.HTTP_400_BAD_REQUEST)

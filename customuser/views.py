from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer, LoginSerializer, UsernameUniqueSerializer
from .models import User

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

# Create your views here.
class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse(
                {
                    "token": token.key
                }
            )
        else:
            return JsonResponse({"message": "로그인 에러"}, status=500)

class UsernameUniqueView(generics.GenericAPIView):

    serializer_class = UsernameUniqueSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        #시리얼라이저의 is_valid 기능을 활용하여 중복여부를 검사한다.
        if serializer.is_valid():
            return JsonResponse({'message': '사용가능한 아이디입니다'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': '중복된 이메일입니다.'}, status=500)
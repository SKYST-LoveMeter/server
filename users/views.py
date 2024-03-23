from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSignUpSerializer
from .models import User
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from django.contrib.auth import authenticate

# 회원가입
class SignUpAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user 생성
        user = User.objects.create_user(**serializer.validated_data)

        # token 생성
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "access": access_token,
                "refresh": refresh_token
            },
            status=status.HTTP_200_OK,
        )

        return res

# 로그인
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 유저 인증
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "access": access_token,
                    "refresh": refresh_token
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    
class UserInfoAPIView(APIView):
    def get(self, request):
        user = request.user

        return Response(
            {
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )

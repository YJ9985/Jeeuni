from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
# from django.contrib.auth.models import BaseUserManager
import random
import string
import requests
import datetime

from .serializers import SignupSerializer, LoginSerializer

User = get_user_model()


class LocalSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'created',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'birth_date': str(user.birth_date),
                    'provider': user.provider,
                }
            }, status=201)
        return Response(serializer.errors, status=400)


class LocalLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return redirect(settings.FRONTEND_LOGIN_URL)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "logged_in",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    'name': user.name,
                    "birth_date": str(user.birth_date),
                    "provider": user.provider,
                }
            }, status=200)
        return Response(serializer.errors, status=400)


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get('access_token')
        birth_date = request.data.get('birth_date')

        if not access_token:
            return Response({'detail': 'access_token is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user_info_url = 'https://www.googleapis.com/oauth2/v1/tokeninfo'
        params = {'access_token': access_token}
        user_info_res = requests.get(user_info_url, params=params)

        if user_info_res.status_code != 200:
            return Response({'detail': 'Invalid Google token.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_res.json()
        email = user_info.get('email')
        if not email:
            return Response({'detail': 'Email not found in Google response.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            created = False
        except User.DoesNotExist:
            if not birth_date:
                return Response({
                    'status': 'need_birth_date',
                    'access_token': access_token,
                    'email': email,
                }, status=202)

            user = User.objects.create_user(
                username=email,
                email=email,
                birth_date=birth_date,
                provider='google',
                password=generate_random_password()
            )
            created = True

        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'created' if created else 'logged_in',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.first_name,
                'birth_date': str(user.birth_date) if user.birth_date else None,
                'provider': user.provider,
            }
        }, status=200)


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get('access_token')
        birth_date = request.data.get('birth_date')

        if not access_token:
            return Response({'detail': 'access_token is required.'}, status=400)

        user_info_url = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        kakao_res = requests.get(user_info_url, headers=headers)

        if kakao_res.status_code != 200:
            return Response({'detail': 'Invalid Kakao token.'}, status=400)

        kakao_data = kakao_res.json()
        kakao_id = kakao_data.get('id')
        kakao_account = kakao_data.get('kakao_account', {})
        profile = kakao_account.get('profile', {})

        email = kakao_account.get('email')
        nickname = profile.get('nickname', '')
        birth_date = request.data.get('birth_date')

        # 카카오 아이디로 가입된 유저 있으면 바로 로그인
        try:
            user = User.objects.get(provider='kakao', kakao_id=kakao_id)
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'logged_in',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'birth_date': str(user.birth_date) if user.birth_date else None,
                    'provider': user.provider,
                }
            }, status=200)
        except User.DoesNotExist:
            if not birth_date:
                return Response({
                    'status': 'need_birth_date',
                    'access_token': access_token,
                    'kakao_id': kakao_id,
                    'nickname': nickname,
                }, status=202)

        # 3. 새 사용자 생성
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=nickname,
            provider='kakao',
            kakao_id=kakao_id,
            password=generate_random_password()
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'created',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'birth_date': str(user.birth_date),
                'provider': user.provider,
            }
        }, status=200)

class UserProfileUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get('access_token')
        birth_str = request.data.get('birth_date')

        if not all([access_token, birth_str]):
            return Response({'detail': 'access_token, and birth_date are required.'}, status=400)
        
        try:
            birth_date = datetime.datetime.strptime(birth_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return Response(
                {'detail': 'birth_date는 YYYY-MM-DD 형식이어야 합니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 먼저 Kakao 시도
        kakao_headers = {'Authorization': f'Bearer {access_token}'}
        kakao_res = requests.get('https://kapi.kakao.com/v2/user/me', headers=kakao_headers)

        if kakao_res.status_code == 200:
            kakao_data = kakao_res.json()
            kakao_id = kakao_data.get('id')
            kakao_account = kakao_data.get('kakao_account', {})
            profile = kakao_account.get('profile', {})
            email = kakao_account.get('email')
            nickname = profile.get('nickname', '')

            if not email:
                return Response({'detail': '카카오에서 이메일을 받지 못했습니다.'}, status=400)

            if User.objects.filter(kakao_id=kakao_id).exists():
                return Response({'detail': '이미 가입된 사용자입니다.'}, status=400)

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=nickname,
                birth_date=birth_date,
                provider='kakao',
                kakao_id=kakao_id,
                password=generate_random_password()
            )

        else:
            # Kakao 실패 → Google 시도
            google_res = requests.get(
                'https://www.googleapis.com/oauth2/v1/tokeninfo',
                params={'access_token': access_token}
            )

            if google_res.status_code != 200:
                return Response({'detail': 'access_token이 유효하지 않습니다.'}, status=400)

            google_data = google_res.json()
            email = google_data.get('email')

            if not email:
                return Response({'detail': '구글에서 이메일을 받지 못했습니다.'}, status=400)

            if User.objects.filter(email=email, provider='google').exists():
                return Response({'detail': '이미 가입된 사용자입니다.'}, status=400)

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=email.split('@')[0],
                birth_date=birth_date,
                provider='google',
                password=generate_random_password()
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'created',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.first_name,
                'birth_date': str(user.birth_date),
                'provider': user.provider,
            }
        }, status=201)
        
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 등록
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class DeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password = request.data.get("password")
        refresh_token = request.data.get("refresh")

        # local 유저는 비밀번호 확인 필요
        if user.provider == "local":
            if not password:
                return Response({"detail": "비밀번호를 입력해주세요."}, status=400)
            if not check_password(password, user.password):
                return Response({"detail": "비밀번호가 일치하지 않습니다."}, status=400)
        else:
            # 소셜 유저 → 본인 인증은 JWT 자체로 확인
            pass  # 추가 확인 로직 필요 시 여기에 삽입 가능 (예: 생년월일 재입력 등) -> 현재로서는 불필요

        # refresh 토큰 무효화
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                return Response({"detail": "유효하지 않은 refresh token입니다."}, status=400)

        # 유저 삭제
        user.delete()
        return Response({"detail": "회원 탈퇴 및 로그아웃 완료."}, status=204)

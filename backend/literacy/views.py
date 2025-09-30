import json
# from backend.accounts import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import EvaluateLiteracySerializer, BookRecommendationsResponseSerializer, LiteracyTestListSerializer
from .models import LiteracyTest
from .utils.level_judge import LiteracyLevelJudge
from .utils.book_recommendation import recommend_books

# @permission_classes([AllowAny])  # 프론트 연동 후 인증 설정 필요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def evaluate_literacy(request):
    # 0) 사용자 이름 정보 수집
    user_name = getattr(request.user, 'name', None)

    # 1) serializer로 입력 검증
    serializer = EvaluateLiteracySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    test_result = serializer.validated_data
    # 2) 판정 로직 호출
    judge = LiteracyLevelJudge()
    result = judge.judge_literacy_level(test_result)

    result['correct_answers'] = result['debug_info']['total_score']
    result['total_questions'] = 15

    # 3) 응답
    return Response({
        'literacy_level':result['literacy_level'],
        'feedback':result['feedback'],
        'recommendation_direction':result['recommendation'],
        'is_exception':result['is_exception'],
        'correct_answers':result['correct_answers'],
        'total_questions':result['total_questions'],
        'debug':result.get('debug_info', {}),
        'userName':request.user.name,
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def recommend_book(request):
    test_result = request.data.get("test_result", {})
    if not test_result:
        return Response({"detail": "test_result required"}, status=status.HTTP_400_BAD_REQUEST)

    # 1) Service 호출
    try:
        raw = recommend_books(test_result)
        data = json.loads(raw)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 2) 응답 검증
    serializer = BookRecommendationsResponseSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def test_literacy(request):
    if request.method == 'GET':
        questions = LiteracyTest.objects.all()
        serializer = LiteracyTestListSerializer(questions, many=True)
        return Response(serializer.data)

from rest_framework import serializers
from .models import LiteracyTest

class ResponseItemSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    is_correct  = serializers.BooleanField()

class EvaluateLiteracySerializer(serializers.Serializer):
    stage_1 = ResponseItemSerializer(many=True, required=False)
    stage_2 = ResponseItemSerializer(many=True, required=False)
    stage_3 = ResponseItemSerializer(many=True, required=False)
    stage_4 = ResponseItemSerializer(many=True, required=False)
    stage_5 = ResponseItemSerializer(many=True, required=False)

    def validate(self, data):
        # 최소 하나의 stage 데이터가 있어야 할 경우
        if not any(k in data and data[k] for k in [f"stage_{i}" for i in range(1,6)]):
            raise serializers.ValidationError("최소 하나 이상의 단계 데이터가 필요합니다.")
        return data
    
class EvaluateLiteracyResponseSerializer(serializers.Serializer):
    literacy_level              = serializers.IntegerField()
    feedback                     = serializers.CharField()
    recommendation_direction    = serializers.CharField()
    is_exception                 = serializers.BooleanField()
    correct_answers              = serializers.IntegerField()
    total_questions              = serializers.IntegerField()
    debug                        = serializers.JSONField(required=False)


class LiteracyResultSerializer(serializers.Serializer):
    literacy_level = serializers.IntegerField()
    feedback       = serializers.CharField()
    recommendation = serializers.CharField()

class BookRecommendationSerializer(serializers.Serializer):
    genre       = serializers.CharField()
    title       = serializers.CharField()
    description = serializers.CharField()
    reason      = serializers.CharField()
    reading_tip = serializers.CharField()

class BookRecommendationsResponseSerializer(serializers.Serializer):
    recommendations = BookRecommendationSerializer(many=True)

class LiteracyTestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiteracyTest
        fields = '__all__'

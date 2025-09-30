from django.db import models
from django.core.exceptions import ValidationError
import jsonschema

# 1) 수정된 JSON 스키마 정의
LEVEL_CRITERIA_SCHEMA = {
    "type": "object",
    "properties": {
        "stage_accuracy": {
            "type": "object",
            "properties": {
                # 각 단계별 정확도 조건
                "stage_1": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["accuracy", "correct_count", "incorrect_count"]},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]}
                    },
                    "required": ["operator", "value", "comparison"]
                },
                "stage_2": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["accuracy", "correct_count", "incorrect_count"]},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]}
                    }
                },
                "stage_3": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["accuracy", "correct_count", "incorrect_count"]},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]}
                    }
                },
                "stage_4": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["accuracy", "correct_count", "incorrect_count"]},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]}
                    }
                },
                "stage_5": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["accuracy", "correct_count", "incorrect_count"]},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]}
                    }
                },
                # 평균 정확도 조건
                "stage_1_2_avg": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["avg_accuracy"]},
                        "stages": {"type": "array", "items": {"type": "integer"}},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]}
                    },
                    "required": ["operator", "stages", "value", "comparison"]
                },
                "stage_1_3_avg": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["avg_accuracy"]},
                        "stages": {"type": "array", "items": {"type": "integer"}},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]}
                    },
                    "required": ["operator", "stages", "value", "comparison"]
                },
                "stage_1_4_avg": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["avg_accuracy"]},
                        "stages": {"type": "array", "items": {"type": "integer"}},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]}
                    },
                    "required": ["operator", "stages", "value", "comparison"]
                }
            },
            "additionalProperties": False
        },
        "total_score": {
            "type": "object",
            "properties": {
                "min": {"type": "integer", "minimum": 0},
                "max": {"type": "integer", "minimum": 0}
            },
            "required": ["min", "max"]
        },
        "priority": {"type": "integer", "minimum": 1, "maximum": 5}
    },
    "required": ["total_score", "priority"],
    "additionalProperties": False
}

EXCEPTION_ALLOWED_SCHEMA = {
    "type": "object",
    "properties": {
        "stage_accuracy": {
            "type": "object",
            "patternProperties": {
                "^stage_[1-5]$|^stage_[1-5]_[1-5]_avg$": {
                    "type": "object",
                    "properties": {
                        "operator": {"type": "string", "enum": ["accuracy", "correct_count", "incorrect_count", "avg_accuracy"]},
                        "value": {"type": "number"},
                        "comparison": {"type": "string", "enum": [">=", "<=", ">", "<", "=="]},
                        "stages": {"type": "array", "items": {"type": "integer"}}
                    },
                    "required": ["operator", "value", "comparison"]
                }
            },
            "additionalProperties": False
        },
        "total_score": {
            "type": "object",
            "properties": {
                "min": {"type": "integer", "minimum": 0},
                "max": {"type": "integer", "minimum": 0}
            },
            "required": ["min", "max"]
        },
        "conditions": {"type": "string"}
    },
    "additionalProperties": False
}

# 2) JSONField 검증기
def validate_level_criteria(value):
    try:
        jsonschema.validate(instance=value, schema=LEVEL_CRITERIA_SCHEMA)
    except jsonschema.ValidationError as e:
        raise ValidationError(f"level_criteria 스키마 오류: {e.message}")

def validate_exception_allowed(value):
    if value is None:
        return
    try:
        jsonschema.validate(instance=value, schema=EXCEPTION_ALLOWED_SCHEMA)
    except jsonschema.ValidationError as e:
        raise ValidationError(f"exception_allowed 스키마 오류: {e.message}")

class LiteracyCriteria(models.Model):
    """
    문해력 수준별 판단 기준 & 피드백/추천
    """
    literacy_level = models.PositiveSmallIntegerField(
        unique=True,
        help_text="문해력 수준 (1~5)"
    )
    level_criteria = models.JSONField(
        validators=[validate_level_criteria],
        help_text="정규 판단 기준(JSON)"
    )
    exception_allowed = models.JSONField(
        null=True,
        blank=True,
        validators=[validate_exception_allowed],
        help_text="예외 허용 조건(JSON, 선택)"
    )
    feedback = models.TextField(
        help_text="해당 수준 피드백"
    )
    recommendation = models.TextField(
        help_text="해당 수준 추천 학습 활동"
    )

    class Meta:
        db_table = "literacy_criteria"
        indexes = [
            models.Index(fields=["literacy_level"], name="idx_literacy_level"),
        ]
        ordering = ["literacy_level"]

    def __str__(self):
        return f"Level {self.literacy_level}"


class LiteracyTest(models.Model):
    """
    문해력 테스트 문제
    """
    question = models.CharField(
        max_length=300,
        help_text="질문 텍스트"
    )
    content = models.TextField(
        null=True,
        blank=True,
        help_text="문제 지문 텍스트"
    )
    img_content = models.ImageField(
        upload_to='literacy_tests/',
        null=True,
        blank=True,
        help_text="문제 지문 이미지"
    )
    choices = models.JSONField(
        help_text="보기 배열, ex. ['30,050','30,500','300,050','300,500']"
    )
    answer = models.PositiveSmallIntegerField(
        help_text="정답 번호 (1~4)"
    )
    level = models.PositiveSmallIntegerField(
        help_text="난이도 레벨 (1~5)"
    )

    class Meta:
        db_table = "literacy_test"
        ordering = ["level", "id"]

    def __str__(self):
        return f"[Lv{self.level}] {self.question[:20]}…"

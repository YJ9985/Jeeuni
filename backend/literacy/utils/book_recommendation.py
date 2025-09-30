import json
from openai import OpenAI

from django.conf import settings
from .level_judge import LiteracyLevelJudge

def get_openai_client():
    api_key = getattr(settings, "OPENAI_API_KEY", "") or ""
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)


PROMPT_TEMPLATE = """
당신은 “청소년·성인 대상 문해력 진단 및 맞춤 도서 큐레이션”에 전문성을 갖춘 국어교육 교수이자 독서 코치입니다.

아래 Input Data를 참고하여, 장르별 도서를 각 1권(문학, 경제, 자기계발, 과학) 추천해주세요.
반환은 반드시 JSON 스키마에 맞추어야 합니다.
추천 도서는 반드시 개인별 literacy_level 을 고려하여 구성하여야 합니다.
reason은 사용자의 feedback, recommendation을 반영한 “~가 하고 싶다면?” 형태로 질문형으로 끝나야 합니다.
reason 응답 예시 : “문단 흐름 파악을 연습하고 싶다면?”

Input Data:
{input_data}

Format:
{{
  "recommendations": [
    {{
      "genre": "문학",
      "title": "도서명",
      "description": "30자 이내 책 소개",
      "reason": "추천 이유",
      "reading_tip": "읽기 팁, 30자 이내"
    }},
    {{
      "genre": "경제",
      "title": "도서명",
      "description": "30자 이내 책 소개",
      "reason": "추천 이유",
      "reading_tip": "읽기 팁, 30자 이내"
    }},
    {{
      "genre": "자기계발",
      "title": "도서명",
      "description": "30자 이내 책 소개",
      "reason": "추천 이유",
      "reading_tip": "읽기 팁, 30자 이내"
    }},
    {{
      "genre": "과학",
      "title": "도서명",
      "description": "30자 이내 책 소개",
      "reason": "추천 이유",
      "reading_tip": "읽기 팁, 30자 이내"
    }}
  ]
}}
"""

def recommend_books(test_result: dict):
    client = get_openai_client()

    # 1) 판정
    judge = LiteracyLevelJudge()
    result = judge.judge_literacy_level(test_result)

    # 2) Input Data 조합
    input_data = {
        "user_profile": {
            "literacy_level":       result["literacy_level"],
            "correct_answers":      result["correct_answers"],
            "total_questions":      result["total_questions"],
            "feedback":             result["feedback"],
            "recommendation_direction": result["recommendation"],
        }
    }
    prompt = PROMPT_TEMPLATE.format(input_data=json.dumps(input_data, ensure_ascii=False))

    # 3) GPT 호출
    resp = client.chat.completions.create(model="gpt-4o-mini",
    messages=[{"role":"system","content":prompt}],
    temperature=0.7)
    return resp.choices[0].message.content

FROM python:3.13-slim

# 1) 기본 파이썬 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 2) 시스템 패키지 설치 (psycopg2 등 DB 드라이버에 필요)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 3) 파이썬 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) 소스 코드 복사
COPY . /app

# 5) 컨테이너에서 열 포트
EXPOSE 8000

# 6) 서버 실행 (WSGI_APPLICATION 에 맞춰서)
CMD ["gunicorn", "mypjt.wsgi:application", "--bind", "0.0.0.0:8000"]

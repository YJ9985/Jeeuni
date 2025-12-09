# 1단계: 빌드
FROM node:20 AS build

WORKDIR /app

COPY vue-project/package*.json ./
RUN npm install

COPY vue-project/ .
RUN npm run build

# 2단계: Nginx로 정적 파일 서빙
FROM nginx:stable

# Nginx 설정 (SPA 라우팅)
COPY ./infra/nginx.conf /etc/nginx/conf.d/default.conf

# Vite 빌드 결과물 복사
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
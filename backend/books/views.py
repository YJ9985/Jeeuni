from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.files.base import ContentFile

import os, requests
from urllib.parse import urlparse
from .utils import detect_text, get_info
from .models import Book, Post, Comment, Category
from .serializers import BookListSerializer, BookSerializer, PostSerializer, PostUpdateSerializer, CommentListSerializer, CommentCreateSerializer, PostCreateSerializer, BookCreateSerializer, PostListSerializer, BookUpdateSerializer, CategoryListSerializer, BookReturnSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def book_list(request):
    if request.method == 'GET':
        books = get_list_or_404(Book)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def book_detail(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list(request, post_pk): 
    post = get_object_or_404(Post, pk=post_pk)
    
    if request.method == 'GET':
        comments = post.comment_set.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':
        # 사용자가 선택한 book_pk를 request.data에서 받음
        book_pk = request.data.get('book_pk')
        if not book_pk:
            return Response({"error": "book_pk는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = get_object_or_404(Book, pk=book_pk)
        except Book.DoesNotExist:
            return Response({"error": "해당 도서를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(book=book, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def book_search(request):
    query = request.GET.get('q', '').strip()

    if query:
        search_result = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
        if not search_result.exists():
            return Response([], status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': '검색어를 입력하세요'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = BookListSerializer(search_result, many=True)
    return Response(serializer.data)


# @csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_upload(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image = image_file.read()

        try:
            result = detect_text(image)
            lines = result[0].description if result else ""
            options = list(set(line.strip() for line in lines.split('\n') if line.strip()))
            return JsonResponse({'options': options})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JsonResponse({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def book_get_info(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        if not q:
            return JsonResponse({'error': 'Missing query parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_books = get_info(q)
            return JsonResponse(new_books)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_create(request):
    if request.method == 'POST':
        data = request.data.copy()
        category_pk = data.get('category')
        category = Category.objects.get(id=category_pk)
        
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            book = serializer.save(category=category)
            return Response(BookReturnSerializer(book).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def category_list(request):

    if request.method == 'GET':
        categories = get_list_or_404(Category)
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)


# 사용자가 작성한 포스트 리스트.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list(request, book_pk):

    if request.method == 'GET':
        posts = Post.objects.filter(user=request.user)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


# 도서 수정 및 삭제는 관리자만 가능.
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def book_update(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)

    if request.method == 'PUT':
        serializer = BookUpdateSerializer(book, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

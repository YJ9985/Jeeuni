from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "health": request.build_absolute_uri("/api/health/"),
        "v1": request.build_absolute_uri("/api/v1/"),
        "v2": request.build_absolute_uri("/api/v2/"),
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def api_v1_root(request):
    return Response({
        "books": request.build_absolute_uri("/api/v1/books/"),
        "categories": request.build_absolute_uri("/api/v1/categories/"),
        "book_search": request.build_absolute_uri("/api/v1/posts/create/books/search/"),
        "book_library": request.build_absolute_uri("/api/v1/posts/create/books/library/"),
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def api_v2_root(request):
    return Response({
        "literacy_test": request.build_absolute_uri("/api/v2/literacy/test/"),
        "literacy_evaluate": request.build_absolute_uri("/api/v2/literacy/evaluate/"),
        "book_recommend": request.build_absolute_uri("/api/v2/books/recommend/"),
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"})

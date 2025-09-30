from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list),
    path('books/<int:book_pk>/', views.book_detail),
    path('posts/<int:post_pk>/', views.post_detail),
    path('posts/<int:post_pk>/comments/', views.comment_list),
    path('posts/<int:post_pk>/comments/<int:comment_pk>/', views.delete_comment),
    path('posts/create/', views.create_post),
    path('posts/create/books/search/', views.book_search),
    path('posts/create/books/upload/', views.book_upload),
    path('posts/create/books/library/', views.book_get_info),
    path('posts/create/books/library/add/', views.book_create),
    path('categories/', views.category_list),
    
    # path('mypage/posts/', views.post_list),
    # path('books/<int:book_pk>/update/', views.book_update),
]

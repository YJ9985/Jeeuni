from django.urls import path
from . import views

urlpatterns = [
    path('literacy/evaluate/', views.evaluate_literacy, name='evaluate-literacy'),
    path('literacy/test/', views.test_literacy),
    path('books/recommend/', views.recommend_book, name='recommend-books'),
]
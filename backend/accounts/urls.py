from django.urls import path, include
from .views import LocalSignupView, LocalLoginView,GoogleLoginView, KakaoLoginView, LogoutView, DeleteView, UserProfileUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', LocalSignupView.as_view(), name='local_signup'),
    path('login/', LocalLoginView.as_view(), name='local_login'),
    path('signup/google/', GoogleLoginView.as_view(), name='google_login_api'),
    path('signup/kakao/', KakaoLoginView.as_view(), name='kakao_login_api'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteView.as_view(), name='logout_delete'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

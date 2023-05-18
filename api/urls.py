from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

app_name = 'article_api'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('category/', views.CategoryAPIView.as_view(), name='category_api'),
    path('article/', views.ArticleAPIView.as_view(), name='article_api'),
    path('predicthand/', views.ImagePredictionView.as_view(), name='predict_hand_api'),
    path('test/', views.test, name='test'),
    path('documentation/', views.documentation, name='documentation')
]
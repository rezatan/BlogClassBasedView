from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from article.models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .rps_model import predict_image
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied

class ImagePredictionView(generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        image_file = request.FILES['image']
        prediction = predict_image(image_file)
        return Response({'prediction': prediction})
        
class CategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        permissions.BasePermission
        ]

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('article.add_category'):
            raise PermissionDenied("User does not have permission to add category.")
        return super().create(request, *args, **kwargs)
        
    def perform_create(self, serializer):
        category_name = serializer.validated_data.get('name')
        if Category.objects.filter(name=category_name).exists():
            raise serializers.ValidationError('Category already exists.')
        serializer.save()

class ArticleAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.BasePermission]

    def create(self, request, *args, **kwargs):
        # Check if the user has the 'article.add_article' permission
        if not request.user.has_perm('article.add_article'):
            raise PermissionDenied("User does not have permission to add articles.")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        body = serializer.validated_data.get('body')
        if Article.objects.filter(title=title).exists():
            raise serializers.ValidationError('Article with that title already exists.')
        elif Article.objects.filter(body=body).exists():
            raise serializers.ValidationError('Article with that content body already exists.')
        serializer.save()

    def get_queryset(self):
        queryset = Article.objects.all()
        title = self.request.query_params.get('title', None)
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__name=category)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset

def test(request):
    return render (request, 'api_test.html')

def documentation(request):
    return render (request, 'api_docs.html')
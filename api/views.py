from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from article.models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .rps_model import predict_image
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
import json

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

    def get_queryset(self):
        queryset = Category.objects.all()
        id = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

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
        category_name = serializer.validated_data.get('category')
        category = get_object_or_404(Category, name=category_name)

        if Article.objects.filter(title=title).exists():
            raise serializers.ValidationError('Article with that title already exists.')
        elif Article.objects.filter(body=body).exists():
            raise serializers.ValidationError('Article with that content body already exists.')
        serializer.save(category=category)

    def get_queryset(self):
        queryset = Article.objects.all()
        id = self.request.query_params.get('id', None)
        title = self.request.query_params.get('title', None)
        category = self.request.query_params.get('category', None)
        is_published = self.request.query_params.get('is_published', None)
        slug = self.request.query_params.get('slug', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if category is not None:
            queryset = queryset.filter(category__name=category)
        if is_published is not None:
            queryset = queryset.filter(is_published=json.loads(is_published))
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset

def test(request):
    return render (request, 'api_test.html')

def documentation(request):
    return render (request, 'api_docs.html')
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from article.models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .rps_model import predict_image

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
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.BasePermission
        ]

    def has_permission(self, request, view):
        return 'category.add_category' in request.auth.scope

    def perform_create(self, serializer):
        category_name = serializer.validated_data.get('name')
        if Category.objects.filter(name=category_name).exists():
            raise serializers.ValidationError('Category already exists.')
        serializer.save()

class ArticleAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.BasePermission
    ]
    def has_permission(self, request, view):
        return 'article.add_article' in request.auth.scope

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
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__name=category)
        return queryset

def testIndex(request):
    return render (request, 'test_index.html')
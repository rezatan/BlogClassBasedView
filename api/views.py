from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from article.models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from .rps_model import predict_image

class ImagePredictionView(generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        image_file = request.FILES['image']
        prediction = predict_image(image_file)
        return Response({'prediction': prediction})
        
class CategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save()

class ArticleAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = Article.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__name=category)
        return queryset

def testIndex(request):
    return render (request, 'test_index.html')
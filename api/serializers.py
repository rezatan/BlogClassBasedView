from rest_framework import serializers
from article.models import Article, Category
from django.utils.text import slugify

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    
    class Meta:
        model = Article
        exclude = ['slug']

    def create(self, validated_data):
        article = Article.objects.create(
            title=validated_data['title'],
            body=validated_data['body'],
            category=validated_data['category']
        )
        article.slug = slugify(article.title)
        article.save()
        return article

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
from django.forms import ModelForm
from django import forms
from .models import Article, Category


class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = [
			'title',
			'body',
			'category',
		]
		widgets = {
            'category' : forms.Select()
        }

class CategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = ['name']
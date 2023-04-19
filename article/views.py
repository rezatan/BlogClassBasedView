from django.shortcuts import render
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	DeleteView, 
	UpdateView
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

# load model
from .models import Article
from .forms import ArticleForm


class ArticleUpdateView(UpdateView):
	form_class = ArticleForm
	model = Article
	template_name = "article/article_update.html"


class ArticleDeleteView(DeleteView):
	model = Article
	template_name = "article/article_delete_confirmation.html"
	success_url = reverse_lazy('article:manage')

@method_decorator(login_required, name='dispatch')
class ArticleManageView(ListView):
	model = Article
	template_name = "article/article_manage.html"
	context_object_name = 'article_list'


class ArticleCreateView(CreateView):
	form_class = ArticleForm
	template_name = "article/article_create.html"


class ArticleEachCategory():
	model = Article
	def get_latest_article_each_category(self):
		category_list = self.model.objects.values_list('category', flat=True).distinct()
		queryset = []

		for category in category_list:
			article = self.model.objects.filter(category=category).latest('published')
			queryset.append(article)

		return queryset
		

class ArticleCategoryListView(ListView):
	model = Article
	template_name = "article/article_category_list.html"
	context_object_name = 'article_list'
	ordering = ['-published']
	paginate_by = 3

	def get_queryset(self):
		self.queryset = self.model.objects.filter(category=self.kwargs['category'])
		return super().get_queryset()

	def get_context_data(self,*args,**kwargs):
		category_list = self.model.objects.values_list('category', flat=True).distinct().exclude(category=self.kwargs['category'])
		self.kwargs.update({'category_list':category_list})
		kwargs = self.kwargs
		return super().get_context_data(*args,**kwargs)	


class ArticleListView(ListView):
    model = Article
    template_name = "article/article_list.html"
    context_object_name = 'article_list'
    ordering = ['-published']
    paginate_by = 3

    def get_context_data(self,*args,**kwargs):
    	category_list = self.model.objects.values_list('category', flat=True).distinct()
    	self.kwargs.update({'category_list':category_list})
    	kwargs = self.kwargs
    	return super().get_context_data(*args,**kwargs)


class ArticleDetailView(DetailView):
	model = Article
	template_name = "article/article_detail.html"
	context_object_name = 'article'

	def get_context_data(self,*args,**kwargs):
		category_list = self.model.objects.values_list('category', flat=True).distinct()
		self.kwargs.update({'category_list':category_list})

		similiar_article = self.model.objects.filter(category=self.object.category).exclude(id=self.object.id)
		self.kwargs.update({'similiar_article':similiar_article})	

		kwargs = self.kwargs
		return super().get_context_data(*args,**kwargs)


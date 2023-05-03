from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	DeleteView, 
	UpdateView
)
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
# load model
from .models import Article, Category
from .forms import ArticleForm, CategoryForm


@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
	permission_required = 'article.change_article'
	form_class = ArticleForm
	model = Article
	template_name = "article/article_update.html"


@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
	permission_required = 'article.delete_article'
	model = Article
	template_name = "article/article_delete_confirmation.html"
	success_url = reverse_lazy('article:manage', args=[1])


@method_decorator(login_required, name='dispatch')
class ArticleManageView(ListView):
	model = Article
	template_name = "article/article_manage.html"
	context_object_name = 'article_list'
	ordering = ['-created']
	paginate_by = 3
	
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
		
	def post(self, *args, **kwargs):
		article_id = self.request.POST.get('article_id')
		article = Article.objects.get(id=article_id)
		article.is_published = not article.is_published
		article.save()
		return self.get(self, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ArticleCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'article.add_article'
	form_class = ArticleForm
	template_name = "article/article_create.html"

@method_decorator(login_required, name='dispatch')
class CategoryCreateView(PermissionRequiredMixin, CreateView):
	permission_required = 'article.add_article'
	form_class = CategoryForm
	template_name = "article/article_add_category.html"
	
	def get_success_url(self):
		return reverse_lazy('article:manage', kwargs={'page': 1})

	def form_valid(self, form):
		name = form.cleaned_data['name']
		if Category.objects.filter(name=name).exists():
			form.add_error('name', 'Category with this name already exists')
			return self.form_invalid(form)
		else:
			category = Category(name=name)
			category.save()
			return redirect(self.get_success_url())

class ArticleEachCategory():
	model = Article

	def get_latest_article_each_category(self):
		category_list = self.model.objects.values_list('category__name', flat=True).distinct()
		queryset = []
		for category in category_list:
			article = self.model.objects.filter(category__name=category, is_published=True).latest('published')
			queryset.append(article)
		return queryset
		

class ArticleCategoryListView(ListView):
	model = Article
	template_name = "article/article_category_list.html"
	context_object_name = 'article_list'
	ordering = ['-published']
	paginate_by = 3

	def get_queryset(self):
		self.queryset = self.model.objects.filter(category__name=self.kwargs['category'])
		self.queryset = self.model.objects.filter(is_published=True)
		return super().get_queryset()

	def get_context_data(self,*args,**kwargs):
		category_list = self.model.objects.values_list('category__name', flat=True).distinct().exclude(category__name=self.kwargs['category'])
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
		category_list = self.model.objects.values_list('category__name', flat=True).distinct()
		print(category_list)
		self.kwargs.update({'category_list':category_list})
		kwargs = self.kwargs
		return super().get_context_data(*args,**kwargs)
		
	def get_queryset(self):
		self.queryset = self.model.objects.filter(is_published=True)
		return super().get_queryset()

class ArticleDetailView(DetailView):
	model = Article
	template_name = "article/article_detail.html"
	context_object_name = 'article'

	def get_context_data(self,*args,**kwargs):
		category_list = self.model.objects.values_list('category__name', flat=True).distinct()
		self.kwargs.update({'category_list':category_list})
		similiar_article = self.model.objects.filter(category=self.object.category).exclude(id=self.object.id)
		self.kwargs.update({'similiar_article':similiar_article})	
		kwargs = self.kwargs
		return super().get_context_data(*args,**kwargs)



from django.views.generic import TemplateView
from django.shortcuts import redirect
from article.views import ArticleEachCategory
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class BlogHomeView(TemplateView, ArticleEachCategory):
	template_name = "index.html"

	def get_context_data(self):
		querysets = self.get_latest_article_each_category()
		context = {
			'latest_artikel_list':querysets,
		}

		return context

class LogoutView(LogoutView):
	next_page = 'login'

class LoginView(LoginView):
	template_name = 'login.html'
	def form_valid(self, form):
        # Log the user in.
		login(self.request, form.get_user())
		return super().form_valid(form)
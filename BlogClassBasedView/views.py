from django.views.generic import TemplateView
from article.views import ArticleEachCategory
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache



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

class LoginView(UserPassesTestMixin, LoginView):
	template_name = 'login.html'

	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def test_func(self):
		return not self.request.user.is_authenticated

	def handle_no_permission(self):
		if self.request.user.groups.filter(name='reader').exists():
			return redirect('home')
		else :
			return redirect('article:manage') 
		
	def get_success_url(self):
		if self.request.user.groups.filter(name='reader').exists():
			return reverse_lazy('home')
		else :
			return reverse_lazy('article:manage')

	def form_valid(self, form):
        # Log the user in.
		login(self.request, form.get_user())
		self.request.session.set_expiry(0)
		return super().form_valid(form)
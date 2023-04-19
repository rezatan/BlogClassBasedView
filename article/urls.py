from django.urls import path
from .views import (
	ArticleListView, 
	ArticleDetailView,
	ArticleCategoryListView,
	ArticleCreateView,
	ArticleManageView,
	ArticleDeleteView,
	ArticleUpdateView,
)

app_name = 'article'
urlpatterns = [
	path('manage/update/<int:pk>', ArticleUpdateView.as_view(), name='update'),
	path('manage/delete/<int:pk>', ArticleDeleteView.as_view(), name='delete'),
	path('manage/', ArticleManageView.as_view(), name='manage'),
	path('create/', ArticleCreateView.as_view(), name='create'),
	path('category/<str:category>/<int:page>', ArticleCategoryListView.as_view(), name='category'),
	path('detail/<slug:slug>', ArticleDetailView.as_view(), name='detail'),
	path('<int:page>', ArticleListView.as_view(), name='list'),
]
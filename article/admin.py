from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	readonly_fields=[
		'slug',
		'updated',
		'published',
	]

admin.site.register(Article, ArticleAdmin)
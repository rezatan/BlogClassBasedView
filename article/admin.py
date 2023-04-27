from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	readonly_fields = [
				'is_published',
				'published',
				'created',
				'updated',
				'slug',	
	]
	def get_readonly_fields(self, request, obj):
		readonly_fields = super().get_readonly_fields(request, obj)
		print(request.user.has_perm('article.publish_article'))
        # If user has 'publish_article' permission, remove 'is_published' from readonly_fields
		if request.user.has_perm('article.publish_article'):
			readonly_fields = list(readonly_fields)
			readonly_fields.remove('is_published')
			readonly_fields = tuple(readonly_fields)
			
		return readonly_fields

admin.site.register(Article, ArticleAdmin)
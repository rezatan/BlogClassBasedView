from django.contrib import admin
# Register your models here.
from .models import Article, Category

class ArticleAdmin(admin.ModelAdmin):
	list_display = ['title', 'category','is_published', 'published', 'updated', 'created']
	def get_readonly_fields(self, request, obj):
		if obj !=None:
			if obj.is_published:
				if request.user.has_perm('article.publish_article'):
					readonly_fields = [
									'title',
									'body',
									'category',
									'created',
									'updated',
									'published',
									'slug',	
									]

				else:
					return [data.name for data in self.model._meta.fields]

			else:
				if request.user.groups.filter(name='publisher').exists():
					readonly_fields = [
									'title',
									'body',
									'category',
									'created',
									'updated',
									'published',
									'slug',	
									]

				elif request.user.has_perm('article.publish_article'):
					readonly_fields = [
							'published',
							'created',
							'updated',
							'slug',	
						]	

				else:
					readonly_fields = [
							'is_published',
							'published',
							'created',
							'updated',
							'slug',	
						]	

		else:
			if request.user.has_perm('article.publish_article'):
				readonly_fields = [
								'created',
								'updated',
								'published',
								'slug',	
								]

			else:
				readonly_fields = [
						'is_published',
						'published',
						'created',
						'updated',
						'slug',	
					]

		return readonly_fields
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'id']
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
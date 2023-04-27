from django.contrib import admin
from django.forms.widgets import CheckboxInput

from django.db import models
# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
	formfield_overrides = {
        models.BooleanField: {'widget': CheckboxInput},
    }
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
					return readonly_fields
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
					return readonly_fields
				elif request.user.has_perm('article.publish_article'):
					readonly_fields = [
							'published',
							'created',
							'updated',
							'slug',	
						]	
					return readonly_fields
				else:
					readonly_fields = [
							'is_published',
							'published',
							'created',
							'updated',
							'slug',	
						]	
				return readonly_fields
		else:
			if request.user.has_perm('article.publish_article'):
				readonly_fields = [
								'created',
								'updated',
								'published',
								'slug',	
								]
				return readonly_fields
			else:
				readonly_fields = [
						'is_published',
						'published',
						'created',
						'updated',
						'slug',	
					]	
			return readonly_fields

		



admin.site.register(Article, ArticleAdmin)
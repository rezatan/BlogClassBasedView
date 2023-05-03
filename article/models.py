from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse_lazy('article:manage', args=[1])
	
		

class Article(models.Model):
	title		= models.CharField(max_length=255)
	body 		= models.TextField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	created		= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	is_published = models.BooleanField(default=False)
	published 	 = models.DateTimeField(null=True)
	slug		 = models.SlugField(blank=True, editable=False)

	class Meta:
		permissions = (
			('publish_article', 'Can publish article'),
		)

	def save(self):
		self.slug = slugify(self.title)
		if self.is_published == True:
			self.published = timezone.now()
		else:
			self.published = None
			
		super().save()

	def get_absolute_url(self):
		url_slug = {'slug':self.slug}
		return reverse('article:detail', kwargs = url_slug)

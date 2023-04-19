from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Article(models.Model):
	title		= models.CharField(max_length=255)
	body 		= models.TextField()
	category_choices = [
		('Test', 'Test'),
		('News', 'News'),
		('Sport', 'Sport'),
	]
	category 	= models.CharField(
		max_length=10,
		choices=category_choices,
		default='Test'
	)
	published	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	slug		= models.SlugField(blank=True, editable=False)

	def save(self):
		self.slug = slugify(self.title)
		super().save()

	def get_absolute_url(self):
		url_slug = {'slug':self.slug}
		return reverse('article:detail', kwargs = url_slug)

	def __str__(self):
		return "{}. {}".format(self.id, self.title)
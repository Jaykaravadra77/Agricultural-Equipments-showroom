from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator

def upload_location(instance, filename):
	file_path = '{author_id}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.Equipment_name), filename=filename)
	return file_path


class BlogPost(models.Model):
	Equipment_name		 = models.CharField(max_length=50, null=False, blank=False,unique=True)
	detail				=     models.TextField(max_length=5000, null=False, blank=False)
	image		 			= models.ImageField(upload_to=upload_location, null=True, blank=False)
	price = models.CharField(  max_length=9, validators=[RegexValidator(r'^\d{1,10}$')])
	availablity            =models.BooleanField(default=True)
	author 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug 					= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.ename
	def delete(self, using=None, keep_parents=False):
		self.image.delete()
		return super().delete(using=using, keep_parents=keep_parents)

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.ename)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)



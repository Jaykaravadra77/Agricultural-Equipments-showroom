from django import forms

from equipments.models import BlogPost 


class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['Equipment_name', 'detail', 'image','price']
	def save(self,commit=True):
		blog_post = self.instance
		blog_post.ename = self.cleaned_data['Equipment_name']
		blog_post.edetail = self.cleaned_data['detail']
		blog_post.eprice = self.cleaned_data['price']
		 
		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']
		if commit:
			blog_post.save()
		return blog_post


class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['Equipment_name','detail','price','availablity','image']

	

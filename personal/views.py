from django.shortcuts import render,redirect,get_object_or_404
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from equipments.views import get_blog_queryset
from equipments.models import BlogPost
from django.contrib import auth
from account.models import Account 
from account.views import get_user_queryset
BLOG_POSTS_PER_PAGE = 4
from django.contrib.auth import login, authenticate, logout
from account.models import State
from account.views import searchform
 
 
def home_screen_view(request, *args, **kwargs):
	
	context = {}

	# Search
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	# blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	


	# # Pagination
	# page = request.GET.get('page', 1)
	# blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	# try:
	# 	blog_posts = blog_posts_paginator.page(page)
	# except PageNotAnInteger:
	# 	blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	# except EmptyPage:
	# 	blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

	# context['blog_posts'] = blog_posts
	
	 
	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, "personal/home.html", context)



def home_screen_viewo(request):
	context = {}
	state=State.objects.all()
	context['state']=state 
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	users= sorted(get_user_queryset(query),key=attrgetter('showroom_name'), reverse=True)
	
	 


	# # Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(users, BLOG_POSTS_PER_PAGE)
	try:
		users = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		users = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		users = blog_posts_paginator.page(blog_posts_paginator.num_pages)
	
	
	 
	if request.user.is_authenticated: 
	 blog_posts = BlogPost.objects.filter(author=request.user)
	 context['blog_posts'] = blog_posts
	 return render(request,'personal/home.html',context)
	context['users'] = users
  
	# context['blog_posts'] = blog_posts

	return render(request,'personal/homeo.html',context)
	 
 
 
def details(request, pk):
	context = {}
	bg=BlogPost.objects.filter(author_id=pk)

	context['users'] = bg
	# context['blog_posts'] = blog_posts
	return render(request,'personal/detailse.html',context)

def detail_blog_view(request, slug):

	context = {}

	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post

	return render(request, 'personal/details_blog.html', context)
def back(request ):
    return redirect("personal/detailse.html")

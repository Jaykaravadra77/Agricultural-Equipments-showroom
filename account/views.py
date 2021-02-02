from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from equipments.models import BlogPost
from account.views import *
from account.models import Account
from django.db.models import Q
from account.models import City
from account.forms import searchform

def registration_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
           form.save()
           email = form.cleaned_data.get('email')
           raw_password = form.cleaned_data.get('password1')
           account = authenticate(email=email, password=raw_password)
           login(request, account)
           return redirect('home')
    return render(request, 'account/register.html', {'form':form})

# def registration_view(request):
# 	context = {}
# 	if request.POST:
# 		form = RegistrationForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			email = form.cleaned_data.get('email')
# 			raw_password = form.cleaned_data.get('password1')
# 			account = authenticate(email=email, password=raw_password)
# 			login(request, account)
# 			return redirect('home')
# 		else:
# 			context['registration_form'] = form

# 	else:
# 		form = RegistrationForm()
# 		context['registration_form'] = form
# 	return render(request, 'account/register.html', context)
 

def logout_view(request):
	logout(request)
	request.session.flush()
	return redirect('/')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

 
	context={}
	if request.POST:
		form = AccountUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"showroom_name": request.POST['showroom_name'],
			}
			form.save()
			context['success_message'] = "Updated"
		else:
			 context['alert'] =form._errors
		
	form = AccountUpdateForm(
			initial = {
					"image":request.user.image	,	
	 				"email": request.user.email, 
					"showroom_name": request.user.showroom_name,
                    "id":request.user.id
     
			}
		)

	context['form'] = form
	return render(request, 'account/account.html', context)



# def account_view(request):

# 	if not request.user.is_authenticated:
# 			return redirect("login")

# 	context = {}
# 	if request.POST:
# 		form = AccountUpdateForm(request.POST, instance=request.user)
# 		if form.is_valid():
# 			form.initial = {
# 					"email": request.POST['email'],
# 					"username": request.POST['username'],
# 			}
# 			form.save()
# 			context['success_message'] = "Updated"
# 	else:
# 		form = AccountUpdateForm(

# 			initial={
# 					"email": request.user.email, 
# 					"username": request.user.username,
# 				}
# 			)

# 	context['account_form'] = form

# 	blog_posts = BlogPost.objects.filter(author=request.user)
# 	context['blog_posts'] = blog_posts

# 	return render(request, "account/account.html", context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})

     
def get_user_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		users = Account.objects.filter(
				Q( city__name__icontains=q)
			
			).distinct()

		for post in users:
			queryset.append(post)

	return list(set(queryset))	
def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id) 
    # return render(request, 'account/city_dropdown_list_options.html', {'cities': cities})
    return JsonResponse(list(cities.values('id', 'name')), safe=False)

def delete(request,pk):
    blog_post = get_object_or_404(Account, id=pk)
    blog_post.delete()
    return redirect("must_authenticate")
 


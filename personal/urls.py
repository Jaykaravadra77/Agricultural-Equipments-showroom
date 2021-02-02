from django.urls import path
from personal.views import (
     detail_blog_view,
       back,
       details
      
    

	# edit_blog_view,
)
 
  

app_name = 'personal'

urlpatterns = [
    path('details/<int:pk>', details, name="details"),
    path('<slug>/', detail_blog_view, name="detaile"),
    path('back', back, name="back"),
    
     
 ]



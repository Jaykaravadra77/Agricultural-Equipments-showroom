from django.urls import path
from account.views import (
    load_cities
)
from account.views import delete
app_name = 'account'

urlpatterns = [
    path('ajax/load-cities/',  load_cities, name='ajax_load_cities'), # AJAX
    path('delete/<int:pk>/',delete,name="deletea")
 ]

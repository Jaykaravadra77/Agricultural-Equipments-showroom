from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from account.models import City,State
from django.forms import ModelForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email','username','showroom_name','State','city','address','showroom_type','contact_no','image','password1','password2' )
         
         
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['city'].queryset = City.objects.none()
        
         if 'State' in self.data:
                 try:
                		country_id = int(self.data.get('State'))
               			self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
                 except (ValueError, TypeError):
                		pass  # invalid input from the client; ignore and fallback to empty City queryset
         elif self.instance.pk:
            		self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

class searchform(forms.ModelForm):
	class Meta:
		model=Account
		fields=('State','city')           
            

	 
class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')
	 
	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('image', 'showroom_name','email','id' )
		widgest={
			'email':forms.EmailInput(attrs={'class':'form-control'})
		}
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('  is already in use.' )

	def clean_showroom_name(self):
		showroom_namee = self.cleaned_data['showroom_name']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(showroom_name=showroom_namee)
		except Account.DoesNotExist:
			return showroom_namee
		raise forms.ValidationError('  is already in use.'  )

 
		 
		 














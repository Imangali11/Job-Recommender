from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .models import Resume



# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class EditUserForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = {"username", "email"}

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('pdf_file',)
from django import forms
from django.core import validators
from .models import MyUser

class FormRegistration(forms.Form):

    username = forms.CharField(required=True,max_length=30,min_length=6)
    email    = forms.EmailField(required=True,max_length=200,widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    phone    = forms.CharField(required=True,max_length=20,min_length=8,validators=[validators.validate_integer])
    password = forms.CharField(required=True,min_length=8,max_length=16)
    password_confirmation = forms.CharField(max_length=16)


    def clean(self):

        #check email
        email = self.cleaned_data.get('email')
        user = MyUser.objects.filter(email=email).first()
        if user is not None:
            self.add_error('email','Email already use!')

        #check password math
        pas = self.cleaned_data.get('password')
        pas_conf = self.cleaned_data.get('password_confirmation')

        if pas != pas_conf:
            self.add_error('password','Passwords Not Math!')

        return True



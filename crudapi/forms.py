from django import forms

class Subscribe(forms.Form):
    Email = forms.EmailField()

    def __str__(self):
        return self.Email

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20) 
    email = forms.EmailField()
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

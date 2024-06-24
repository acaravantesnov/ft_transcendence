from django import forms

class newUser(forms.Form):
    username = forms.CharField(max_length=15, label="Username",
                               widget=forms.TextInput(
                                   attrs={
                                       'class':'form-control',
                                       'placeholder':'username'
                                       }))
    first_name = forms.CharField(max_length=15, label="Firstname",
                               widget=forms.TextInput(
                                   attrs={
                                       'class':'form-control',
                                       'placeholder':'name...'
                                       }))
    last_name = forms.CharField(max_length=15, label="Lastname",
                               widget=forms.TextInput(
                                   attrs={
                                       'class':'form-control',
                                       'placeholder':'last name...'
                                        }))
    email = forms.EmailField(required=True, label="email",
                             widget=forms.EmailInput(
                                 attrs={
                                     'class':'form-control',
                                     'placeholder':'user@42.com'
                                     }))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class':'form-control',
                                       'placeholder':'*******'
                                       }))
    confirm_password = forms.CharField(label="Repeat password",
                                       widget=forms.PasswordInput(
                                       attrs={
                                           'class':'form-control',
                                           'placeholder':'*******'
                                           }))
    avatar = forms.ImageField(label="Avatar",
                              widget=forms.FileInput(
                                  attrs={
                                      'class':'form-control'
                                  }))
    

class signUser(forms.Form):
    username = forms.CharField(max_length=15, label="Username",
                               widget=forms.TextInput(
                                   attrs={
                                       'class':'form-control',
                                       'placeholder':'username',
                                       }))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class':'form-control',
                                       'placeholder':'********'
                                       }))

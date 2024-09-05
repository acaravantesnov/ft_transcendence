from django import forms
from .models import MyCustomUser

# class newUser(forms.Form):
#     username = forms.CharField(max_length=15, label="Username", 
#                                 widget=forms.TextInput(
#                                     attrs={
#                                         'class':'form-control',
#                                         'placeholder':'username'
#                                 }))
#     first_name = forms.CharField(max_length=15, label="Firstname", 
#                                 widget=forms.TextInput(
#                                     attrs={
#                                         'class':'form-control',
#                                         'placeholder':'name...'
#                                 }))
#     last_name = forms.CharField(max_length=15, label="Lastname",
#                                 widget=forms.TextInput(
#                                     attrs={
#                                         'class':'form-control',
#                                         'placeholder':'last name...'
#                                 }))
#     email = forms.EmailField(required=True, label="email",
#                                 widget=forms.EmailInput(
#                                     attrs={
#                                         'class':'form-control',
#                                         'placeholder':'user@42.com'
#                                 }))
#     password = forms.CharField(label="Password",
#                                 widget=forms.PasswordInput(
#                                     attrs={
#                                         'class':'form-control',
#                                         'placeholder':'*******'
#                                 }))
#     confirm_password = forms.CharField(label="Repeat password",
#                                 widget=forms.PasswordInput(
#                                     attrs={
#                                         'class':'form-control',
#                                         'placeholder':'*******'
#                                 }))
#     avatar = forms.ImageField(label="Avatar", required=False,
#                                 widget=forms.FileInput(
#                                     attrs={
#                                         'class':'form-control'
#                                 }))
    

class newUser(forms.ModelForm):
    confirm_password = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*******'}))
    
    class Meta:
        model = MyCustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'name...'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'last name...'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'user@42.fr.com'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'*******'}),
            'avatar': forms.FileInput(attrs={'class':'form-control'}),
        }
    
    preferred_language = forms.CharField(max_length=10, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = True
        self.fields['confirm_password'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match. Please enter matching passwords.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'preferred_language' in self.cleaned_data:
            instance.preferred_language = self.cleaned_data['preferred_language']
        instance.set_password(self.cleaned_data["password"])
        if commit:
            instance.save()
        return instance


class updateProfileInfo(forms.Form):
    username = forms.CharField(max_length=15, label="Username",
                                widget=forms.TextInput(
                                    attrs={
                                        'class':'form-control',
                                        'placeholder':'username',
                                }))
    first_name = forms.CharField(label="First Name",
                                widget=forms.TextInput(
                                    attrs={
                                        'class':'form-control',
                                        'placeholder':'Juanito'
                                }))
    last_name = forms.CharField(label="Last Name",
                                widget=forms.TextInput(
                                    attrs={
                                        'class':'form-control',
                                        'placeholder':'Garcia'
                                }))
    email = forms.CharField(label="Email",
                                widget=forms.TextInput(
                                    attrs={
                                        'class':'form-control',
                                        'placeholder':'newMail@42.fr'
                                }))


class newPassword(forms.Form):
    currentPassword = forms.CharField(label="Current password",
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class':'form-control',
                                        'placeholder':'********',
                                }))
    newPassword = forms.CharField(label="New password",
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class':'form-control',
                                        'placeholder':'********'
                                }))
    confirmPassword = forms.CharField(label="Confirm password",
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class':'form-control',
                                        'placeholder':'********'
                                }))

class updateAvatarForm(forms.ModelForm):
    class Meta:
        model = MyCustomUser
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', False)

        if avatar:
            if avatar.size > 2*1024*1024:
                raise forms.ValidationError("Avatar file too large ( > 2mb )")
            return avatar
        else:
            raise forms.ValidationError("Couldn't read uploaded image")
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.avatar = self.cleaned_data["avatar"]
        if commit:
            instance.save()
        return instance

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

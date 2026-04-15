from django import forms
from django.contrib.auth.models import User
from .models import Contact, UserProfile


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)
    email      = forms.EmailField(required=True)
    phone      = forms.CharField(max_length=15, required=False)
    password1  = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2  = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.email      = self.cleaned_data['email']
        if commit:
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone', '')
            profile.save()
        return user


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name  = forms.CharField(max_length=50, required=False)
    email      = forms.EmailField(required=False)
    phone      = forms.CharField(max_length=15, required=False)
    address    = forms.CharField(max_length=200, required=False)

    class Meta:
        model  = UserProfile
        fields = ['phone', 'address']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial  = self.user.last_name
            self.fields['email'].initial      = self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name  = self.cleaned_data.get('last_name', '')
            self.user.email      = self.cleaned_data.get('email', '')
            if commit:
                self.user.save()
        profile.phone   = self.cleaned_data.get('phone', '')
        profile.address = self.cleaned_data.get('address', '')
        if commit:
            profile.save()
        return profile

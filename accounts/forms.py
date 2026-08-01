from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class BuyerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = False
        if commit:
            user.save()
        return user

class VendorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    rip = forms.CharField(max_length=50, required=True, label="RIP (Relevé d'Identité Postal/Bancaire)")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = True
        if commit:
            user.save()
            user.profile.rip = self.cleaned_data.get('rip')
            user.profile.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number')

class ProfileDetailUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar', 'rip')
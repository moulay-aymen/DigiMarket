from django import forms 
from .models import Product , Profile


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name' , 'image', 'desc' , 'category' , 'file' , 'price']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo' , 'bio' , 'phone' , 'mail' , 'BaridiMob']
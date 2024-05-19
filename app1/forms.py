# import profile

from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from .models import Profile, Subcategory, Product, Product_Gallary, CartAdd


class RegistrationForm(SignupForm):
    class Meta():
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].label = 'Display Name'
            self.fields['Email'].label = "Email Address"


class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile

        fields = ['picture', 'id']

        labels = {'picture': ''}


class ProductForm(forms.ModelForm):
    class Meta():
        model = Product

        fields = ['Image', 'id']

        labels = {'Image': ''}


class ProductGallaryForm(forms.ModelForm):
    class Meta():
        model = Product_Gallary

        fields = ['Image1', 'Image2', 'Image3', 'id']

        labels = {'Image1': ''}


class CartAddForm(forms.ModelForm):
    class Meta():
        model = CartAdd
        fields = ['quantity']
        labels = {'quantity': ''}


class SubcategoryForm(forms.ModelForm):
    class Meta():
        model = Subcategory
        fields = "__all__"

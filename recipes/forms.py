from django import forms
from django.forms import inlineformset_factory

from .models import Product
from .models import Recipe, RecipeProduct


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'unit']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name']


RecipeProductFormSet = inlineformset_factory(
    Recipe, RecipeProduct,
    fields=('product', 'quantity'),
    extra=1,
    can_delete=False
)

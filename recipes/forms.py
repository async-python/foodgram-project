from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tag', 'cooking_time', 'description', 'image',)
        widgets = {
            'tag': CheckboxSelectMultiple(),
        }

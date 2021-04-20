from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from recipes.models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Recipe
        fields = ('name', 'tag', 'cooking_time', 'description', 'image',)
        widgets = {
            'tag': CheckboxSelectMultiple,
        }

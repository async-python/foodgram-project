from django import forms
from recipes.models import Recipe, Tag, Ingredient


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )

    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(), to_field_name="name"
    )

    class Meta:
        model = Recipe
        fields = (
            'name', 'cooking_time', 'description',
            'image',
            # 'tag', 'ingredients',
        )

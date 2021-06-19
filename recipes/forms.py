from django import forms
from django.db import transaction
from django.forms.widgets import CheckboxSelectMultiple

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        to_field_name='title'
    )
    amount = {}

    class Meta:
        model = Recipe
        fields = (
            'name', 'tag', 'ingredients', 'cooking_time', 'description',
            'image',)
        widgets = {
            'tag': CheckboxSelectMultiple(),
        }

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            index_ingredient = 0
            for item in list(data):
                if item.startswith('nameIngredient_'):
                    data.update(
                        {
                            'ingredients': data.get(item),
                        })
                elif item.startswith('valueIngredient_'):
                    self.amount[
                        data.getlist('ingredients')[
                            index_ingredient]] = data.get(
                        item)
                    index_ingredient += 1
        super().__init__(data, *args, **kwargs)

    def save(self, commit=True):
        with transaction.atomic():
            recipe_obj = super().save(commit=False)
            recipe_obj.save()
            recipe_obj.recipe_ingredients.all().delete()
            ingredients_amount = self.amount
            recipe_obj.recipe_ingredients.set(
                [
                    RecipeIngredient(
                        recipe=recipe_obj, ingredient=ingredient,
                        amount=ingredients_amount[ingredient.title]
                    )
                    for ingredient in self.cleaned_data['ingredients']
                ],
                bulk=False)
            self.amount = {}
            self.save_m2m()
            return recipe_obj

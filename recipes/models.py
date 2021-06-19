from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=255, db_index=True, unique=True, verbose_name='Title')
    dimension = models.CharField(
        max_length=20, db_index=True, verbose_name='Dimension')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'Ingredient name: {self.title}, dimension {self.dimension}'


class Tag(models.Model):
    name = models.CharField(max_length=50, null=True, verbose_name='Name')
    slug = models.SlugField(
        max_length=50, null=True, unique=True, verbose_name='Slug')
    color = models.CharField(
        max_length=50, null=True, verbose_name='Check box color')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'Tag: {self.name}'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Recipe name',
        max_length=255,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Recipe`s author',
        on_delete=models.CASCADE,
        related_name='recipes',
        db_index=True
    )
    description = models.TextField(verbose_name='Recipe description')
    cooking_time = models.PositiveIntegerField(
        validators=(
            MinValueValidator(0, message='The value must be greater than 0'),
        ),
        verbose_name='Cooking time'
    )
    image = models.ImageField(upload_to='recipes/', verbose_name='Image')
    created = models.DateTimeField(
        auto_now=True, verbose_name='Time publication')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ingredients'
    )
    tags = models.ManyToManyField(Tag, related_name='recipe_tag', )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-created']

    def __str__(self):
        return f'Recipe name: {self.name}, author: {self.author}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ingredient')
    amount = models.PositiveIntegerField(verbose_name='Amount')

    class Meta:
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipe Ingredients'


class SubscriptionUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='User'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author'
    )

    class Meta:
        verbose_name = 'Subscription User'
        verbose_name_plural = 'Subscription Users'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique subscription of an auth user'),
        )

    def __str__(self):
        return f'User: {self.user}, author: {self.author}'

    def is_following(self, author_id):
        response = SubscriptionUser.objects.select_related(
            'user', 'author'
        ).filter(
            user=self.id, author=author_id
        ).exists()
        return response


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Recipe'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='User'
    )

    class Meta:
        verbose_name = 'Favorite Recipe'
        verbose_name_plural = 'Favorite Recipes'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique favorite list of an auth user'),
        )

    def __str__(self):
        return f'User: {self.user}, favorite recipe: {self.recipe.name}'


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_list',
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User'
    )

    class Meta:
        verbose_name = 'Shopping List'
        verbose_name_plural = 'Shopping Lists'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique shopping list of an auth user'),
        )

    def __str__(self):
        return f'User: {self.user}, recipe_id: {self.recipe.id}'


class ShoppingListSession(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_list_session',
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, verbose_name='Session')

    class Meta:
        verbose_name = 'Shopping List Session'
        verbose_name_plural = 'Shopping List Sessions'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'session'),
                name='unique shopping list of an not auth user'),
        )

    def __str__(self):
        return f'User: {self.session}, recipe_id: {self.recipe.id}'

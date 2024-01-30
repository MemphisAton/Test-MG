from django.db import models


class Product(models.Model):
    UNIT_CHOICES = [
        ('g', 'граммы'),
        ('pcs', 'штуки'),
        ('ml', 'миллилитры')
    ]

    name = models.CharField(max_length=100)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='g')
    recipe_count = models.IntegerField(default=0)
    objects: models.Manager = models.Manager()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)

    objects: models.Manager = models.Manager()

    def __str__(self):
        recipe_products = self.recipeproduct_set.all()
        product_descriptions = [
            f"{rp.product.name} {rp.quantity}{rp.product.unit}"
            for rp in recipe_products
        ]
        products_str = ', '.join(product_descriptions)
        return f"{self.name}: {products_str}" if product_descriptions else self.name

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    objects: models.Manager = models.Manager()

    class Meta:
        unique_together = ('recipe', 'product')

    def __str__(self):
        return f"{self.recipe.name} - {self.product.name}"

from django.contrib import admin

from .models import Product
from .models import Recipe, RecipeProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'unit')
    list_display_links = ('name',)


@admin.register(RecipeProduct)
class RecipeProductAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'quantity')


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    list_display_links = ('__str__',)
    inlines = [RecipeProductInline]

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import ProductForm
from .forms import RecipeForm, RecipeProductFormSet
from .models import Product
from .models import Recipe
from .models import RecipeProduct


def add_product_to_recipe(request):
    try:
        recipe_id = request.GET.get('recipe_id')
        product_id = request.GET.get('product_id')
        weight = request.GET.get('weight')

        try:
            weight = float(weight)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Вес должен быть числом'}, status=400)

        if not all([recipe_id, product_id, weight]):
            return JsonResponse({'status': 'error', 'message': 'Некорректные данные'}, status=400)

        recipe = Recipe.objects.get(id=recipe_id)
        product = Product.objects.get(id=product_id)

        recipe_product, created = RecipeProduct.objects.update_or_create(
            recipe=recipe,
            product=product,
            defaults={'quantity': weight}
        )

        return JsonResponse({'status': 'success', 'message': 'Продукт добавлен в рецепт'})

    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Рецепт или продукт не найден'}, status=404)


def cook_recipe(request):
    """
    Увеличивает used_count каждого продукта в рецепте.
    """
    recipe_id = request.GET.get('recipe_id')
    if not recipe_id:
        return JsonResponse({'status': 'error', 'message': 'No recipe_id provided'}, status=400)

    recipe = get_object_or_404(Recipe, id=recipe_id)

    for product in recipe.recipeproduct_set.all():
        product.product.recipe_count += 1
        product.product.save()

    return JsonResponse({'status': 'success'})


def show_recipes_without_product(request):
    """
    Возвращает страницу со списком рецептов, в которых отсутствует указанный продукт.
    Принимает параметр product_id через GET-запрос. Исключает рецепты, где продукт
    присутствует в количестве 10 грамм и более.
    """
    product_id = request.GET.get('product_id')
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'Product ID not provided'}, status=400)

    product = get_object_or_404(Product, id=product_id)

    recipes = Recipe.objects.exclude(
        recipeproduct__product=product,
        recipeproduct__quantity__gte=10
    )

    return render(request, 'recipes/recipes_without_product.html', {'recipes': recipes})


def add_or_update_product(request):
    """
    Обрабатывает POST-запрос для добавления нового продукта или обновления существующего.
    Использует форму ProductForm для валидации данных. Если продукт с таким именем уже существует,
    увеличивает его количество; в противном случае создает новый продукт.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            quantity = form.cleaned_data['quantity']
            unit = form.cleaned_data['unit']

            name_lower = name.lower()

            product, created = Product.objects.get_or_create(
                name__iexact=name_lower,
                defaults={'name': name_lower, 'quantity': quantity, 'unit': unit}
            )

            if not created:
                product.quantity += quantity
                product.save()

            return redirect('home')

    else:
        form = ProductForm()

    return render(request, 'recipes/add_or_update_product.html', {'form': form})


def home(request):
    """
    Отображает главную страницу приложения. Выводит списки всех продуктов и рецептов.
    Продукты сортируются по названию в убывающем порядке.
    """
    products = Product.objects.all().order_by('-name')
    recipes = Recipe.objects.all()

    return render(request, 'recipes/home.html', {'products': products, 'recipes': recipes})


@receiver(post_save, sender=RecipeProduct)
def increase_product_recipe_count(sender, instance, created, **kwargs):
    """
    Сигнал для увеличения счетчика recipe_count продукта при создании нового RecipeProduct.
    Вызывается после сохранения объекта RecipeProduct.
    """
    if created:
        product = instance.product
        product.recipe_count += 1
        product.save()


@receiver(post_delete, sender=RecipeProduct)
def decrease_product_recipe_count(sender, instance, **kwargs):
    """
    Сигнал для уменьшения счетчика recipe_count продукта при удалении RecipeProduct.
    Вызывается после удаления объекта RecipeProduct.
    """
    product = instance.product
    product.recipe_count -= 1
    product.save()


def add_or_edit_recipe(request, recipe_id=None):
    """
    Обрабатывает добавление нового рецепта или редактирование существующего.
    Если recipe_id предоставлен, редактирует существующий рецепт. В противном случае создает новый.
    Использует RecipeForm и RecipeProductFormSet для управления данными рецепта и связанными продуктами.
    """
    if recipe_id:
        recipe = Recipe.objects.get(id=recipe_id)
    else:
        recipe = None

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeProductFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect('home')
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeProductFormSet(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {'form': form, 'formset': formset, 'recipe_id': recipe_id})


def add_recipe(request):
    """
    Обрабатывает создание нового рецепта. Использует RecipeForm и RecipeProductFormSet
    для управления данными рецепта и его продуктами. После успешного создания рецепта
    происходит перенаправление на главную страницу.
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeProductFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            formset.instance = recipe
            formset.save()
            return redirect('home')
    else:
        form = RecipeForm()
        formset = RecipeProductFormSet()

    return render(request, 'recipes/add_recipe.html', {'form': form, 'formset': formset})


def delete_recipe(request, recipe_id):
    """
    Обрабатывает запрос на удаление рецепта. Если запрос выполнен методом POST,
    удаляет рецепт с указанным recipe_id и перенаправляет на главную страницу.
    В противном случае перенаправляет обратно на страницу редактирования рецепта.
    """
    if request.method == 'POST':
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.delete()
        return redirect('home')

    return redirect('edit_recipe', recipe_id=recipe_id)

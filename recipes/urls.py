from django.urls import path

from . import views

urlpatterns = [
    path('add_product_to_recipe/', views.add_product_to_recipe, name='add_product_to_recipe'),
    path('cook_recipe/', views.cook_recipe, name='cook_recipe'),
    path('show_recipes_without_product/', views.show_recipes_without_product, name='show_recipes_without_product'),
    path('add_or_update_product/', views.add_or_update_product, name='add_or_update_product'),
    path('recipe/<int:recipe_id>/', views.add_or_edit_recipe, name='edit_recipe'),
    path('recipe/new/', views.add_or_edit_recipe, name='new_recipe'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('recipe/delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('', views.home, name='home'),

]

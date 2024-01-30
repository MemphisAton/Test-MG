
# Приложение "Поварская книга" на Django

**Это приложение "Поварская книга" разработано в рамках тестового задания 
MirGovorit backend. Приложение реализовано на Django и представляет 
собой систему для управления рецептами и продуктами.**

## Основные Функции
### Приложение включает в себя следующие основные функции:

- **Управление продуктами и рецептами в админке Django:**

В админ-панели можно добавлять, редактировать и удалять продукты и рецепты.

- **В админ-панели можно добавлять, редактировать и удалять продукты и рецепты.
Добавление продукта в рецепт (add_product_to_recipe):**

Добавление продукта в рецепт с указанием веса через HTTP GET-запрос.
Возможность изменения веса продукта, если он уже есть в рецепте.

- **Добавление продукта в рецепт с указанием веса через HTTP GET-запрос.
Возможность изменения веса продукта, если он уже есть в рецепте.
Приготовление рецепта (cook_recipe):**

Увеличение количества приготовлений продукта при приготовлении рецепта.

- **Показ рецептов без определенного продукта (show_recipes_without_product):**

Отображение списка рецептов, в которых отсутствует указанный продукт или его количество меньше 10 грамм.

## Технические Детали
### Модели
- **Product:** 

представляет продукт с полями для названия, количества в базе и количества использований в рецептах.

- **Recipe:** 

представляет рецепт, содержащий название и набор продуктов.

- **RecipeProduct:** 

связывает продукты с рецептами и содержит информацию о количестве каждого продукта в рецепте.

## Установка и Запуск
**Для запуска приложения выполните следующие шаги:**

- Клонируйте репозиторий:
> git clone https://github.com/MemphisAton/Test-MG.git

- Установите зависимости:
> pip install -r requirements.txt

- Выполните миграции:
> python manage.py migrate

- Запустите сервер разработки:
>  manage.py runserver

## Тестирование GET-запросов через браузер
Для тестирования функционала приложения, который обрабатывает GET-запросы, 
вы можете использовать обычный веб-браузер. Вот как вы можете это сделать:

### Тестирование функции add_product_to_recipe
Откройте веб-браузер и введите URL в следующем формате:

> http://127.0.0.1:8000/add_product_to_recipe/?recipe_id=<IDрецепта>&product_id=<IDпродукта>&weight=<вес>
 
Замените <ID рецепта>, <ID продукта> и <вес> на реальные значения.

Нажмите Enter, чтобы отправить запрос. В ответ должно появиться сообщение об успешном добавлении или обновлении продукта в рецепте.

### Тестирование функции cook_recipe
Введите URL для приготовления рецепта:

> http://127.0.0.1:8000/cook_recipe/?recipe_id=<IDрецепта>

Замените <ID рецепта> на реальный идентификатор рецепта.

После отправки запроса должно появиться подтверждение об успешном увеличении количества приготовлений продуктов.

### Тестирование функции show_recipes_without_product
Введите URL для отображения рецептов без определенного продукта:

> http://127.0.0.1:8000/show_recipes_without_product/?product_id=<IDпродукта>

Замените <ID продукта> на идентификатор интересующего вас продукта.

На открывшейся странице будет отображаться список рецептов, 

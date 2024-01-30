# Generated by Django 5.0.1 on 2024-01-30 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_remove_recipeproduct_weight_recipeproduct_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=[('g', 'граммы'), ('pcs', 'штуки'), ('ml', 'миллилитры')], default='g', max_length=10),
        ),
    ]

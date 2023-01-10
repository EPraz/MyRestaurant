from django.contrib import admin
from .models import Ingredient, Purchase, RecipeRequirement, MenuItem

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Purchase)
admin.site.register(RecipeRequirement)
admin.site.register(MenuItem)
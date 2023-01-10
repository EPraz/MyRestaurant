from django.db import models


# Create your models here.
class Ingredient(models.Model):
    """
    Represents a single ingredient in the restaurant's inventory
    """
    # Creating options for cook units
    name = models.CharField(max_length = 200, unique=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=200)
    price_per_unit = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/ingredients'

    def __str__(self):
        return f'''
        name = {self.name};
        qty = {self.quantity};
        unit = {self.unit};
        p/u = {self.price_per_unit};
        '''


class MenuItem(models.Model):
    """
    Represents an entry off the restaurant's menu
    """
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/menu'

    def __str__(self):
        return f"""
        title = {self.title};
        price = {self.price};
        """

    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())


class RecipeRequirement(models.Model):
    """
    This model represents a single ingredient and how much of it is required for an item off the menu.
    """
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    # ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return f"""
        item = {self.menu_item};
        ingr = {self.ingredient};
        qty = {self.quantity};
        """

    def get_absolute_url(self):
        return "/menu"

    def enough(self):
        return self.quantity <= self.ingredient.quantity # if the quantity needed is lesser or equal to the amount on the inventory


class Purchase(models.Model):
    """
    It represents a customer purchase of an item off the menu
    """
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # id = models.Index()
    orders = models.IntegerField(default=1)

    def __str__(self):
        return f"""
        prod = {self.menu_item};
        time = {self.timestamp};
        orders = {self.orders};
        """

    def get_absolute_url(self):
        return '/purchase'
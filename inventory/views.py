from django.shortcuts import redirect, render

from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientForm, MenuItemForm,  RecipeRequirementForm, PurchaseForm

from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from django.db.models import Sum

# Create your views here.
# @login_required
class HomeView(TemplateView):
    template_name  = 'inventory/index.html'

    def get_context_data(self, **kwargs): 
        # KeyWords Arguments
        context = super().get_context_data(**kwargs)#returns a object that represents the parent class
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()       

        return context

# View Section
class MenuView(TemplateView):
    template_name = 'inventory/menu.html'
    model = MenuItem
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.all()
        context['RecipeRequirements'] = RecipeRequirement.objects.all()
        context['Ingredients'] = Ingredient.objects.all()
        return context

# class MenuView( ListView):
#     template_name = "inventory/menu_list.html"
#     model = MenuItem

class IngredientView(LoginRequiredMixin, ListView):
    template_name = "inventory/ingredient.html"
    model = Ingredient
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["ingredients"] = Ingredient.objects.all()
    #     return context

class PurchasesView(ListView):
    template_name = "inventory/purchase_list.html"
    model = Purchase
    
class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/reports.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.all()

        revenue = Purchase.objects.aggregate(revenue = Sum("menu_item__price"))['revenue']
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.price_per_unit * recipe_requirement.quantity

        context['revenue'] = revenue
        context['total_cost'] = total_cost
        context['profit'] = revenue - total_cost



        return context


# CreateView Section


class IngredientCreate(LoginRequiredMixin, CreateView):
    template_name = 'inventory/add_ingredients.html'
    form_class = IngredientForm
    model = Ingredient

class MenuItemCreate(LoginRequiredMixin,  CreateView):
    template_name = 'inventory/add_menu_item.html'
    form_class = MenuItemForm
    model = MenuItem



class NewPurchase(CreateView):
    model = Purchase
    template_name = 'inventory/new_order.html'
    form_class = PurchaseForm

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['menu_items'] = [X for X in MenuItem.objects.all() if X.available()]

        # total_cost = 0.0
        # for purchase in MenuItem.objects.all():
            # total_cost += purchase.price


        # context['total_cost'] = total_cost
        return context

    

    def post(self,  request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item = menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect('/purchases')



# Update Section
# class MenuUpdate(UpdateView):
#     template_name = 'inventory/update_menu.html'
#     model = MenuItem
#     form_class = MenuItemForm

class UpdateIngredientView(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/update_ingredient.html'
    model = Ingredient
    form_class = IngredientForm

class UpdateMenuItem(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/update_menu.html'
    model = MenuItem
    form_class = MenuItemForm

class RecipeRequirementUpdate(LoginRequiredMixin, CreateView):
    template_name = 'inventory/add_recipe_requirement.html'
    model = RecipeRequirementForm
    form_class = RecipeRequirementForm



# Delete Section
class DeleteMenuItem(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'inventory/menu_item_delete_form.html'
    success_url = "/menu/"

class DeleteIngredient(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/delete_ingredient.html"
    success_url = '/inventory/ingredients/'


def log_out(request):
    logout(request)
    return redirect("/")
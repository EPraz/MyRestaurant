from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("logout/", views.log_out, name="logout"),
    path("account/login/", auth_views.LoginView.as_view(), name="login"),
    path("", views.HomeView.as_view(), name="home"),
    # Ingredients
    path('inventory/ingredients/', views.IngredientView.as_view(), name="ingredients"),
    path('inventory/ingredients/new/', views.IngredientCreate.as_view(), name="add_ingredients"),
    path('inventory/ingredients/<slug:pk>/update', views.UpdateIngredientView.as_view(), name="update_ingredient"),
    path('inventory/ingredients/<slug:pk>/recipe_requirement', views.RecipeRequirementUpdate.as_view(), name="add_recipe_requirement"),
    path('inventory/ingredients/<slug:pk>/delete', views.DeleteIngredient.as_view(), name="delete_ingredient"),
    # Menu
    path("menu/", views.MenuView.as_view(), name="menu"),
    path("menu/<slug:pk>/update", views.UpdateMenuItem.as_view(), name="update_menu_item"),
    path("menu/<slug:pk>/update", views.UpdateMenuItem.as_view(), name="update_menu_item"),
    path("menu/menu/new", views.MenuItemCreate.as_view(), name="add_menu_item"),
    path("menu/<slug:pk>/delete", views.DeleteMenuItem.as_view(), name="delete_menu_item"),
    
    # purchase
    path("order/", views.NewPurchase.as_view(), name="new_purchase"),
    path("purchases/", views.PurchasesView.as_view(), name="purchases"),

    # Report
    path("reports", views.ReportView.as_view(), name="reports")

]

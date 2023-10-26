from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("ledger", views.ledger, name='ledger'),
    path("addPiggyBank", views.addPiggyBank, name='addPiggyBank'),
    path("addLineItem", views.addLineItem, name='addLineItem'),
    path("addGoal", views.addGoal, name='addGoal'),
    path("delete/<int:id>", views.deleteLineItem, name="delete"),
    path('register', views.register, name='register'),
]
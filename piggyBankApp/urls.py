from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("ledger/", views.ledger, name='ledger'),
    path("addPiggyBank/", views.addPiggyBank, name='addPiggyBank'),
    path("addLineItem", views.addLineItem, name='addLineItem'),
    path("delete/<int:id>", views.deleteLineItem, name="delete"),

]
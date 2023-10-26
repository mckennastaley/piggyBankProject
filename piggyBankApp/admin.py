from django.contrib import admin
from .models import PiggyBank, LineItem, Goal, Parent, Child


# Register your models here.
admin.site.register(PiggyBank)
admin.site.register(LineItem)
admin.site.register(Goal)
admin.site.register(Parent)
admin.site.register(Child)

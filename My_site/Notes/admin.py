from django.contrib import admin
from .models import User_information,Items_Category,Token
# Register your models here.
admin.site.register(User_information)
admin.site.register(Items_Category)
admin.site.register(Token)
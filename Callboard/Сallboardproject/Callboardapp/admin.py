from django.contrib import admin
from .models import Author, Category, Call, Response

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Call)
admin.site.register(Response)

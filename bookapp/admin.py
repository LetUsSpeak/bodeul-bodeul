from django.contrib import admin

# Register your models here.
from bookapp.models import Book, Paragraph

admin.site.register(Book)
admin.site.register(Paragraph)
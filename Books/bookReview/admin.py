from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'category', 'subcategory', 'publish_date')
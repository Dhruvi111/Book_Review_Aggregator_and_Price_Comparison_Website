from django.contrib import admin
from .models import Book, Contact, UserSignup, favouriteBook, UserReview

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'category', 'subcategory', 'publish_date')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('msg_id', 'fullname', 'email','subject', 'text')

@admin.register(UserSignup)
class UserSignupAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'fullname', 'username', 'email')

@admin.register(favouriteBook)
class favouriteBookAdmin(admin.ModelAdmin):
    list_display = ('current_user', 'book_id_db', 'book_from_api', 'book_id_api')

@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('current_user', 'bookId', 'reviewText', 'date')


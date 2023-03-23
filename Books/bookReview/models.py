from django.db import models
from requests import request
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default="")            # Bestseller, fiction, fantasy, children
    subcategory = models.CharField(max_length=50, default="")         # Belongs to bestseller but also to another categroy like children
    publisher = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=5000, default="")
    publish_date = models.IntegerField(default=0)
    pages = models.IntegerField(default=0)
    isbn_10 = models.CharField(max_length=50, default=0)
    isbn_13 = models.CharField(max_length=50, default=0)
    image = models.ImageField(upload_to='bookReview/images', default="")


    def __str__(self):
        return str(self.book_id)
    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, default="")   
    subject = models.CharField(max_length=300, default="")
    text = models.CharField(max_length=700, default="")

    @property
    def fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)


class UserSignup(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, default="") 
    
    @property
    def fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)
    

class favouriteBook(models.Model):
    current_user = models.ForeignKey(User, on_delete=models.CASCADE)

    book_id_db = models.ForeignKey(Book, blank=True, null=True, on_delete=models.CASCADE)
    book_from_database = models.BooleanField()

    book_from_api = models.BooleanField()
    book_id_api = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        unique_together = [['current_user', 'book_id_db'],['current_user', 'book_id_api']]
       
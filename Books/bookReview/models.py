from django.db import models

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
    image = models.ImageField(upload_to='bookReview/images', default="")


    def __str__(self):
        return self.title
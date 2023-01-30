from django.shortcuts import render, HttpResponse
from .models import Book
from math import ceil

# Create your views here.
def index(request):
    allBooks = []
    # run the folowing two lines and for loop one by one in shell and print the variables to get the idea of what is happening
    category_books = Book.objects.values('category', 'book_id')
    cats = {item['category'] for item in category_books}
    for cat in cats:
        product = Book.objects.filter(category=cat)
        n = len(product)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allBooks.append([product, range(1, nSlides), nSlides])
    params={'allBooks':allBooks }
    # print(allBooks)
    return render(request, "bookReview/index.html", params)

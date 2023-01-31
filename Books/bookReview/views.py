from django.shortcuts import render, HttpResponse
from .models import Book
from math import ceil

# Create your views here.
def index(request):
    allBooks = []
    # run the folowing two lines and for loop one by one in shell and print the variables to get the idea of what is happening
    category_books = Book.objects.values('category', 'book_id')
    cats = {item['category'] for item in category_books}

    # Display books by subcategory
    # subcategory_books = Book.objects.values('subcategory', 'book_id')
    # sub_cats = {item['subcategory'] for item in subcategory_books}

    for cat in cats:
        product = Book.objects.filter(category=cat)
        n = len(product)
        nSlides = n//6 + ceil((n/6) - (n//6))
        allBooks.append([product, range(1, nSlides), nSlides])

    # for sub_cat in sub_cats:
    #     product = Book.objects.filter(subcategory=sub_cat)
    #     n = len(product)
    #     nSlides = n//4 + ceil((n/4) - (n//4))
    #     allBooks.append([product, range(1, nSlides), nSlides])
    params={'allBooks':allBooks }
    # print(allBooks)
    return render(request, "bookReview/index.html", params)


def about(request):
    return render(request, "bookReview/about.html")

def contact(request):
    return render(request, "bookReview/contact.html")
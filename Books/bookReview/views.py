import requests
from django.shortcuts import render, HttpResponse
from .models import Book
from math import ceil
from bs4 import BeautifulSoup
    
# Create your views here.
def api(query, data):
    titles = []
    pic = []
    author = []
    category = []

    json_data = data.json()
    results = json_data['totalItems']
    if len(query) >= 3 and results != 0:
        
        list_items = json_data['items']

        for i in range(len(list_items)):
            volInfo = list_items[i]['volumeInfo']
            # Titles
            if('title' in volInfo):
                arr = volInfo['title'] 
                titles.append(arr)      
            else:
                titles.append("Title Not Available")
            
            # Images
            if('imageLinks' in volInfo):
                arr1 = volInfo['imageLinks']['thumbnail']
                pic.append(arr1)
            else:
                pic.append("/static/bookReview/images/coverNF.png")

            #Authors
            if('authors' in volInfo):
                arr2 = volInfo['authors'] 
                author.append(arr2)      
            else:
                author.append(["Author Info Not Available"])

            #Categories
            if ('categories' in volInfo):
                arr3 = volInfo['categories']
                category.append(arr3)
            else:
                category.append(["Category Info Not Available"])

        length = range(len(titles))
        params = {'titles': titles, 'pic':pic, 'length': length, 'author': author, 'results':results, 'msg':"Search Results", 'gen':'Genre: ', 'category':category, 'query':query}
   

    elif len(query) == 0 or len(query) < 3:
        params={'msg':"Please Enter More Than 3 Letters !"}

    else:
        params = {'msg': "No Results Found", 'query': query}
    return params

# def gettext():
#     url = 'http://127.0.0.1:8000/'
#     r = requests.get(url)
#     htmlContent = r.content
#     soup = BeautifulSoup(htmlContent, 'html.parser')
#     text = []
#     for tag in soup.find_all('a',{"class":"dropdown-item"}):
#         text.append(tag.text)
#     return text

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

def search(request):
    # The API provides maximum 40 results -- search by booknames
    query = request.GET.get('text')
    data = requests.get("https://www.googleapis.com/books/v1/volumes?q=intitle:" + query+"&printType=books&maxResults=36")

    x = api(query=query, data=data)  # x has the value of params
    return render(request, "bookReview/search.html", x)



def genre(request, category):
    
    query = category
    # if query in text:
    data = requests.get("https://www.googleapis.com/books/v1/volumes?q=subject:" + query+"&printType=books&maxResults=36")
    x = api(query=query, data=data)
    #  print(x)
    return render(request, "bookReview/genre.html", x)


def login(request):
    return render(request, "bookReview/login.html")
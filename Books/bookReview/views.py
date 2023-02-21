import requests
from django.shortcuts import render, HttpResponse
from .models import Book, Contact
from math import ceil
from django.contrib import messages
# from bs4 import BeautifulSoup
    
# Create your views here.
def api(query, data):
    titles = []
    pic = []
    author = []
    category = []
    isbn = []
    identifiers = []

    # print("Data:", data)   # gives status code
    json_data = data.json()
    # print("Json Data:", json_data)   # gives data in json format
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

            #ISBN
            # if ('industryIdentifiers' in volInfo):
            #     isbn_type = volInfo['industryIdentifiers'][0]['type']
            #     if isbn_type == "ISBN_13" or isbn_type == "ISBN_10":
            #         arr4 = volInfo['industryIdentifiers'][0]['identifier']
            #         isbn.append(arr4)
                
            #     else:
            #         isbn.append('isbn not found')
            # else:
            #     isbn.append("industry identifiers unavailable")

           
            #id
            if ('id' in list_items[i]):
                arr5 = list_items[i]['id']
                identifiers.append(arr5)
            else:
                identifiers.append("id not found")
        length = range(len(titles))
        params = {'titles': titles, 'pic':pic, 'length': length, 'author': author, 'results':results, 'msg':"Search Results", 'gen':'Category: ', 'category':category, 'query':query, 'isbn':isbn, 'identifiers':identifiers}
        # print(">>>>>>>>",identifiers)

    elif len(query) == 0 or len(query) < 3:
        params={'msg':"Please Enter More Than 3 Letters !"}

    else:
        params = {'msg': "No Results Found", 'query': query}

    return params


def specificBook(data):
    json_data = data.json()
    volInfo = json_data['volumeInfo']
    if('title' in volInfo):
        title = volInfo['title']
    else:
        title = "Oopsie! Title Not Available"

    if('authors' in volInfo):    
        author_list = volInfo['authors']
    else:
        author_list = ["Oopsie! Author Info Not Available"]
    
    if('publisher' in volInfo):
        publisher = volInfo['publisher']
    else:
        publisher = "Oopsie! Publisher Info Not Available"

    if('publishedDate' in volInfo):
        edition = volInfo['publishedDate']
    else:
        edition = "Oopsie! Info Not Available"

    if('description' in volInfo):
        desc = volInfo['description']
    else:
        desc = "Oopsie! Description Not Available"

    if('imageLinks' in volInfo):
        image = volInfo['imageLinks']['thumbnail']
    else:
        image = "/static/bookReview/images/coverNF.png"
        
    if('pageCount' in volInfo):
        no_pages = volInfo['pageCount']
    else:
        no_pages = "Oopsie! Info Not Available"

    display = {'title': title, 'author_list': author_list, 'publisher': publisher, 'edition':edition, 'desc':desc, 'image': image, 'no_pages': no_pages}

    return display


# for landing page
def index(request):
    allBooks = []
    category_books = Book.objects.values('category', 'book_id')
    # print("Category_books", category_books)
    cats = {item['category'] for item in category_books}
    # print("Cats", cats)


    # Display books by subcategory
    # subcategory_books = Book.objects.values('subcategory', 'book_id')
    # sub_cats = {item['subcategory'] for item in subcategory_books}

    for cat in cats:
        product = Book.objects.filter(category=cat)
        n = len(product)
        nSlides = n//6 + ceil((n/6) - (n//6))
        allBooks.append([product, range(1, nSlides), nSlides])
    # print("Product", product)
    # print("Allbooks", allBooks) 

    # for sub_cat in sub_cats:
    #     product = Book.objects.filter(subcategory=sub_cat)
    #     n = len(product)
    #     nSlides = n//4 + ceil((n/4) - (n//4))
    #     allBooks.append([product, range(1, nSlides), nSlides])
    params={'allBooks':allBooks }
    # print(allBooks)
    return render(request, "bookReview/index.html", params)


# for about page
def about(request):
    return render(request, "bookReview/about.html")


# for contact page
def contact(request):
    if request.method == "POST":
      # gets the details through 'name' attribute
      first_name = request.POST.get('fname')
      last_name = request.POST.get('lname')
      email = request.POST.get('email')  
      subject = request.POST.get('subject')   
      text = request.POST.get('text')
      contact = Contact(first_name=first_name,last_name=last_name, email=email,subject=subject, text=text)
      contact.save()
      messages.success(request, 'Your message has been sent sucessfully!')
    return render(request, "bookReview/contact.html")


# for search page
def search(request):
    # The API provides maximum 40 results -- search by booknames
    query = request.GET.get('text')
    data = requests.get("https://www.googleapis.com/books/v1/volumes?q=intitle:" + query + "&printType=books&maxResults=36")

    x = api(query=query, data=data)  # x has the value of params
    return render(request, "bookReview/search.html", x)
  

# for respective genres
def genre(request, category):   
    query = category
    global genre
    genre = category
    data = requests.get("https://www.googleapis.com/books/v1/volumes?q=subject:" + query+"&printType=books&maxResults=36")
    x = api(query=query, data=data)
    #  print(x)
    return render(request, "bookReview/genre.html", x)


# for detailed view
def details(request): 
    num = request.GET.get('id')
    data = requests.get("https://www.googleapis.com/books/v1/volumes/" + num)
    y = specificBook(data=data)
    
    return render(request, "bookReview/details.html", y)



def login(request):
    return render(request, "bookReview/login.html")


# for pagination -- wont work for previous and next buttons yet
# pretty static as of now
def pages(request, digit):
    index = digit

    if index == -1:
        pass  
    if index == 1:
        startIndex = "0"
        print("index=1")
    elif index == 2:
        startIndex = "36"
        print("index=2")

    elif index == 3:
        startIndex = "71"
        print("index 3")

    data = requests.get("https://www.googleapis.com/books/v1/volumes?q=subject:" + genre + "&startIndex=" + startIndex +"&printType=books&maxResults=36")
    x = api(query=genre, data=data)
    return render(request, "bookReview/page.html", x)
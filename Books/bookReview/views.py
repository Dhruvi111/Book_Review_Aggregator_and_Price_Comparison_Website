import requests
from django.shortcuts import render, HttpResponse
from .models import Book, Contact, UserSignup
from math import ceil
from django.contrib import messages
from bs4 import BeautifulSoup
    
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

            # ISBN
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
        params = {'titles': titles, 'pic':pic, 'length': length, 'author': author, 'results':results, 'msg':"Search Results", 'gen':'Category: ', 'category':category, 'query':query, 'identifiers':identifiers}


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

        if '\'' in title:
            title_for_url = title.replace('\'', '%27')
        else:
            title_for_url = title

        if ' ' in title:
            title_for_bmarks = title_for_url.replace(' ', '-')
            print(title_for_bmarks)
        else:
            title_for_bmarks = title

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

    if ('industryIdentifiers' in volInfo):
        isbn_index0 = volInfo['industryIdentifiers'][0]['type']
        isbn_index1 = volInfo['industryIdentifiers'][1]['type']

        if isbn_index0 == "ISBN_13":
            isbn13 = volInfo['industryIdentifiers'][0]['identifier']
            
            if isbn_index1 == "ISBN_10":
                isbn10 = volInfo['industryIdentifiers'][1]['identifier']
            else:
                isbn10 = 'isbn not found'


        elif isbn_index0 == "ISBN_10" :
            isbn10 = volInfo['industryIdentifiers'][0]['identifier']

            if isbn_index1 == "ISBN_13":
                isbn13 = volInfo['industryIdentifiers'][1]['identifier']
            else:
                isbn13 = 'isbn not found'
    else:
        isbn10 = "industry identifiers unavailable"
        isbn13 = "industry identifiers unavailable"

    # print(isbn_index0)
    # print(isbn_index1)
    # print(isbn10)
    # print(isbn13)


    display = {'title': title, 'author_list': author_list, 'publisher': publisher, 'edition':edition, 'desc':desc, 'image': image, 'no_pages': no_pages, 'isbn10':isbn10, 'isbn13': isbn13, 'title_for_url': title_for_url, 'title_for_bmarks': title_for_bmarks}

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


# for detailed view (Landing page)
def detailsHome(request):
    id = request.GET.get('bookId')
    
    book = Book.objects.filter(book_id=id)    # gives queryset
    bookInfo = book.values()     # gives all the values for a particular queryset
    # print(">>>>>>", bookInfo)
    
    for val in bookInfo:        # val gives dictionary
        title = val['title']
        if '\'' in title:
            title_for_url = title.replace('\'', '%27')
        else:
            title_for_url = title  

        if ' ' in title:
            title_for_bmarks = title_for_url.replace(' ', '-')
            print(title_for_bmarks)
        else:
            title_for_bmarks = title
        

        author =  val['author']
        publisher =  val['publisher']
        publish_date = val['publish_date']
        no_pages = val['pages']
        image = val['image']
        desc = val['description']
        isbn10 = val['isbn_10']
        isbn13 = val['isbn_13']



    display = {'title':title, 'author': author, 'publisher': publisher, 'publish_date': publish_date, 'no_pages': no_pages, 'image': image, 'desc': desc, 'isbn10': isbn10, 'isbn13': isbn13, 'title_for_url': title_for_url, 'title_for_bmarks': title_for_bmarks}
    return render(request, "bookReview/detailsHome.html", display)


def login(request):
    return render(request, "bookReview/login.html")

def signup(request):
    if request.method == "POST":
      # gets the details through 'name' attribute
      first_name = request.POST.get('fname')
      last_name = request.POST.get('lname')
      email = request.POST.get('email')  
      username= request.POST.get('uname')   
     
      user = UserSignup(first_name=first_name,last_name=last_name,username=username, email=email)
      user.save()
      messages.success(request, 'Your account has been created sucessfully!')
    return render(request, "bookReview/signup.html")


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


def BNoble(request):  
    isbn_no = request.GET.get('no')
    title = request.GET.get('t')
    author = request.GET.get('a')
    test = "Barnes & Noble review page" 

    url = 'https://www.barnesandnoble.com/w/{title}{author}/?ean={isbn_no}'.format(title=title, author=author, isbn_no=isbn_no)
    # print(url)
    
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0', 
        }
    )

    if isbn_no != "isbn not found" and isbn_no != "industry identifiers unavailable":

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('div', class_='editorial-reviews')
        # print(s)

        if s != None:
            bquote = s.find('blockquote')
            # reviews = bquote.find_all('p')
            msg = ""
        else:
            bquote = " "
            msg = "Couldn't fetch reviews"
       
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", reviews)

    else:
        bquote = " "
        msg = "Couldn't find book on Barnes and Noble. Sorry for the inconvenience !"
 
    bnoble = True
    params = {'test':test, 'title': title, 'author': author, 'isbn_no': isbn_no, 'reviews':bquote , 'msg': msg, 'bnoble': bnoble}
    return render(request, "bookReview/reviews.html", params)


def Bookmarks(request):  
    test = "Bookmarks review page"
    title = request.GET.get('t')
    url = 'https://bookmarks.reviews/reviews/all/{}/'.format(title)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find_all('div', class_='bookmarks_a_review_pullquote')

    # Reviews
    if len(s) != 0:
        review_list = s
        msg = ""
        list_length = range(len(s))
    else:
        review_list = []
        list_length = 0
        msg = "Couldn't fetch reviews"
    # print(">>>>>>>>", review_list)

    # Reviewers
    s1 = soup.select("[itemprop='author']")
    reviewers = []
    for el in s1:
        reviewers.append(el.text)

    # Sources
    s2 = soup.select("[itemprop='sameAs']")
    review_source = []
    for el in s2:
        review_source.append(el.text)

    # print(reviewers)
    # print(review_source)
 
    bookmarks = True
    return render(request, "bookReview/reviews.html", {'test':test, 'bookmarks': bookmarks, 'title': title, 'review_list': review_list, 'msg': msg, 'list_length': list_length, 'reviewers': reviewers, 'review_source': review_source})


def Amazon(request):  
    test = "Amazon review page"
    amazon = True
    return render(request, "bookReview/reviews.html", {'test':test, 'amazon': amazon})


def Goodreads(request):   
    test = "Goodreads review page"
    title_GR = request.GET.get('t')
    author_GR = request.GET.get('a')
    url = ' https://www.goodreads.com/search?q={}&ref=nav_sb_noss_l_15'.format(title_GR)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.select("[itemprop='name']")
    s1 = soup.find_all('a', class_="authorName") 
   
    author_list = []
    for span in s1:
        author_list.append(span.text)
    
    title_list = []
    for el in s:
        title_list.append(el.text)
    
    # ---------------
    # print(author_list)
    # print(author_GR)
    # print("author_list[0] == author_GR",author_list[0] == author_GR)
    # print(title_list[0])
    # print(title_GR)
    # print("title_list[0] == title_GR",title_list[0] == title_GR)

    for i in range(len(title_list)):
        if title_list[i] == title_GR and author_list[i] == author_GR:
            href_list = [a['href'] for a in soup.find_all('a', class_="bookTitle", href=True)]
            required_href = href_list[i]
            break
        else:
            required_href = "not found"

    if required_href != "not found":
        url_book = 'https://www.goodreads.com' + required_href
        r1 = requests.get(url_book)
        new_soup = BeautifulSoup(r1.content, 'html.parser')
        s1 = new_soup.find_all('div', class_="TruncatedContent__text TruncatedContent__text--large")
        
        spans = [span.text for span in s1]
    else:
        msg = "Couldn't fetch reviews"
    # print(">>>>>>>>", spans)
   
    
    goodreads = True
    return render(request, "bookReview/reviews.html", {'test':test, 'title_GR': title_GR, 'goodreads': goodreads})

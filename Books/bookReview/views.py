import requests
from django.shortcuts import redirect, render, HttpResponse
from .models import Book, Contact
from math import ceil
from django.contrib import messages
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 

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

    book_id_api = json_data['id']
    # print(book_api_id)

    volInfo = json_data['volumeInfo']
    if('title' in volInfo):
        title = volInfo['title']

        if '\'' in title:
            title_for_url = title.replace('\'', '%27')
        else:
            title_for_url = title

        if ' ' in title:
            title_for_bmarks = title_for_url.replace(' ', '-')
            # print(title_for_bmarks)
        else:
            title_for_bmarks = title

    else:
        title = "Oopsie! Title Not Available"

    if('authors' in volInfo):    
        author_list = volInfo['authors']
    else:
        author_list = ["Oopsie! Author Info Not Availab le"]
    
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


    display = {'title': title, 'author_list': author_list, 'publisher': publisher, 'edition':edition, 'desc':desc, 'image': image, 'no_pages': no_pages, 'isbn10':isbn10, 'isbn13': isbn13, 'title_for_url': title_for_url, 'title_for_bmarks': title_for_bmarks, 'book_id_api': book_id_api}

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
    book_id_db = request.GET.get('id')
    
    book = Book.objects.filter(book_id=book_id_db)    # gives queryset
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
            # print(title_for_bmarks)
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



    display = {'title':title, 'author': author, 'publisher': publisher, 'publish_date': publish_date, 'no_pages': no_pages, 'image': image, 'desc': desc, 'isbn10': isbn10, 'isbn13': isbn13, 'title_for_url': title_for_url, 'title_for_bmarks': title_for_bmarks, 'book_id_db': book_id_db}
    return render(request, "bookReview/detailsHome.html", display)


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(username=username, password=pwd)

        if user is not None:
            login(request, user)
            fname = user.first_name
            lname = user.last_name

            messages.success(request, 'Logged In sucessfully!')
            return render(request, "bookReview/login.html")
            # return render(request, "bookReview/index.html", {'fname': fname, 'lname': lname})
            # redirct ma proper nai aavtu
        
        else:
            messages.error(request, "Sorry, the login credentials you entered are incorrect. Please try again or reset your password.")
            return render(request, "bookReview/login.html")

    return render(request, "bookReview/login.html")

def signup(request):
    if request.method == "POST":
      # gets the details through 'name' attribute
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')  
        username= request.POST.get('uname')  
        pwd = request.POST.get('pwd')
        pwd2 = request.POST.get('pwd2')
     
    #   user = UserSignup(first_name=first_name,last_name=last_name,username=username, email=email)
    #   user.save()

        myuser = User.objects.create_user(username, email, pwd)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, 'Your account has been created sucessfully!')
        return redirect('signin/')

    return render(request, "bookReview/signup.html")


def signout(request):
    logout(request)
    messages.success(request, 'Logged out sucessfully!')
    # return redirect('signin')
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
            # stars = soup.find_all('div', class_='bv_stars_component_container')
            # stars = soup.find_all('polygon')
            # print(">>>>>>>>", stars)
           
            msg = ""
        else:
            bquote = " "
            msg = "Couldn't fetch reviews"   

    else:
        bquote = " "
        msg = "Couldn't find book on Barnes and Noble. Sorry for the inconvenience !"
    


    # print(">>>>>>", bquote)
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
    # s = soup.select("[itemprop='name']")
    s = soup.select("[role='heading']")
    s1 = soup.find_all('a', class_="authorName") 
   
    author_list = []
    for span in s1:
        author_list.append(span.text)
    
    title_list = []
    for el in s:
        title_list.append(el.text)
    
    # ---------------
    # print(author_list)
    # print(len(author_list))
    # print(author_GR)
    # print("author_list[0] == author_GR",author_list[0] == author_GR)
    # print(title_list[0])
    # print(title_list)
    # print(len(title_list))
    # print(title_GR)
    # print("title_list[0] == title_GR",title_list[0] == title_GR)

    for i in range(len(title_list)):
        if title_list[i] == title_GR:
            if author_list[i] == author_GR:
                href_list = [a['href'] for a in soup.find_all('a', class_="bookTitle", href=True)]
                required_href = href_list[i]
                break
        
            else:
                required_href = "not found"
        else:
            required_href = "not found"

    if required_href != "not found":
        flag = 1
        url_book = 'https://www.goodreads.com' + required_href
        r1 = requests.get(url_book)
        new_soup = BeautifulSoup(r1.content, 'html.parser')
        s1 = new_soup.find_all('div', class_="TruncatedContent__text TruncatedContent__text--large")
        
        names_list = new_soup.find_all('div', class_="ReviewerProfile__name")
        name_text = [a.text for a in names_list]
        # print(name_text)

        review_span = [span.text for span in s1]
        # print("review-span: ", review_span)  
        review_span.pop(0)
        # length = [len(i) for i in review_span]
        short_reviews = []
        reviewer = []
        for i in range(len(review_span)):
            if len(review_span[i]) <= 2000:
                reviewer.append(name_text[i])
                short_reviews.append(review_span[i])
                msg = ""
            else:
                msg = "no reviews found"
                # short_reviews = []
                # reviewer = []

        print(">>>>>>", short_reviews)
        spans_length = range(len(short_reviews))

    else:
        flag = 0
        msg = "Couldn't fetch reviews"
        spans_length = 0
        short_reviews = []
        reviewer = []
        # print("else exec") 
    # print(">>>>>>>>", spans)
   
    
    goodreads = True
    return render(request, "bookReview/reviews.html", {'test':test, 'title_GR': title_GR, 'goodreads': goodreads, 'short_reviews': short_reviews, 'spans_length': spans_length, 'reviewer': reviewer, 'msg': msg, 'flag': flag})


# Doesn't work
# def LibraryThing(request):
#     test = "Google books review page"
#     title = request.GET.get('t')
#     url = 'https://www.booksamillion.com/p/Spare/Prince-Harry-Duke-Sussex/9780593593806?id=8788922522560'
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'html.parser')  
#     s = soup.find_all('h2', class_="pr-faceoff-title")
#     # s = soup.select("[data-workid]")
#     print(s)
 

#     libraryThing = True
#     return render(request, "bookReview/reviews.html", {'test': test, 'libraryThing':libraryThing, 'title': title})


def favourites(request):
    if request.method == "POST":
        hidden_bookId = request.POST.get('value')
        print(hidden_bookId)
    return render(request, "bookReview/userProfile.html")
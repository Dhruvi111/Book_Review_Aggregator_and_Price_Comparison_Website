from django import forms
import requests
from django.shortcuts import redirect, render, HttpResponse
from .models import Book, Contact, favouriteBook, UserReview
from math import ceil
from django.contrib import messages
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
import re
from urllib.request import Request, urlopen
from django.views.decorators.cache import cache_control
# from .forms import UpdateReviewForm

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


def specificBook(request, data):
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

    if request.user.is_authenticated:
        if favouriteBook.objects.filter(book_id_api=book_id_api, current_user=request.user).exists():
            fav = True
            # print(fav)
        else:
            fav = False
            # print(fav)
    else:
        fav = None

    if UserReview.objects.filter(bookId=book_id_api).exists():
        val = UserReview.objects.filter(bookId=book_id_api).values()

        review = []
        date = []
        username = []
        primary_key = []
        
        for i in range(len(val)):
            review.append(val[i]['reviewText'])
            date.append(val[i]['date'])
            current_user_id = val[i]['current_user_id']
            username.append((User.objects.get(id=current_user_id)).username)
            primary_key.append(val[i]['reviewId'])
        
        review_length = range(len(review))
        

    else:
        review = 0
        date = 0
        username = 0
        review_length = 0
        primary_key = 0

    # price_print = price(request)
    # price_len = range(len(price_print))
    # # print(price_len)
    # print(price_print)


    display = {'title': title, 'author_list': author_list, 'publisher': publisher, 'edition':edition, 'desc':desc, 'image': image, 'no_pages': no_pages, 'isbn10':isbn10, 'isbn13': isbn13, 'title_for_url': title_for_url, 'title_for_bmarks': title_for_bmarks, 'book_id_api': book_id_api, 'fav': fav, 'review': review, 'date': date, 'username': username, 'review_length': review_length, 'primary_key': primary_key}

    return display

# ------------------------------ PRICES WITHOUT LINK --------------------------------
# def price(request):
#     # root = "https://www.google.com/"
#     book_name = request.GET.get('title')
#     formatted_book_name = book_name.replace(" ", "+")

#     link = f"https://www.google.com/search?q={formatted_book_name}&tbm=shop"

#     req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
#     webpage = urlopen(req).read()
#     prices = []
#     with requests.Session() as c:
#         soup = BeautifulSoup(webpage, 'html5lib')
#         # print(soup)
#         for item in soup.find_all('div', attrs={'class':'dD8iuc'}): 
#             item = str(item)
#             # print(item)
#             pattern = r'â‚¹(.*?)</div>'
#             result = re.search(pattern, item)
#             if result:
#                 specific_name = result.group(1)
#                 # print(specific_name)
#                 pattern_new = re.sub(r'</span>', '', specific_name)
#                 prices.append(pattern_new)
#                 # print(pattern_new)
#         # print(len(prices))
#         # price_len = len(prices)
#         # return price_len
#     return prices



# ------------------------------ PRICES WITH LINK --------------------------------
def price(request):
    # root = "https://www.google.com/"
    book_name = request.GET.get('title')
    formatted_book_name = book_name.replace(" ", "+")

    link = f"https://www.google.com/search?q={formatted_book_name}&tbm=shop"

    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    prices = []
    price_list = []

    for price in prices:
        price_listinloop = []
        price_listinloop.append(price)
        price_list.append(price_listinloop)

    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html5lib')
        # print(soup)
        count = 0
        for item in soup.find_all('div', attrs={'class':'P8xhZc'}):
            item = str(item)
            # print(item, "\n\n")
            pattern = r'q=(.*?)delivery'
            result = re.search(pattern, item)
            if result:
                specific_name = result.group(1)
                # print(specific_name, "\n\n")
                pattern_new = re.sub(r'">(.*?)¹', ' ', specific_name)
                # print(pattern_new, "\n\n")
                pattern_second = re.sub(r'</span>', "", pattern_new)
                # print(pattern_second, "\n\n")
                pattern_final = re.sub(r'<(.*?)Free', "", pattern_second)
                # print(pattern_final, "\n\n")
                # only_link = re.sub(' (.*?)$', "", pattern_final)
                # # print(only_link, "\n\n")

                # pattern_without_link = re.sub(r'https(.*?) ', "", pattern_final)
                # # print(pattern_without_link, "\n\n")

                # only_name = re.sub(r'https(.*?)from ', "", pattern_final)
                # # print(only_name, "\n\n")

                # a = pattern_final.split()
                # print(a, "\n\n")

                def create_hyperlink(name, url, book_price):
                    name = name.split('<')[0] if '<span' in name else name
                    hyperlink = '<a href="{0}">{1}</a>'.format(url, name)
                    # print(">>>>",name)
                    return '{0} {1}'.format(book_price, hyperlink)

                website_name = pattern_final.split(' from ')[1]
                if website_name in ["PokemonCardSeller", "biblio.co.uk/bookseller_info.ph ...", "The Manan ", "Biblio.com - St Vinnie's ...", "Urdu Bazaar", "Biblio.com-rascal books", "used Etsy", "Read and Rise Book Shop", "BooksTech", "Best Of Used Books", "KoolSkool The Bookstore ", "Apni Kitaben", "Poshmark India - Poshmark", "Online College Street", "Gyaan Store", "Google Play ", "Biblio.com - KnC Books", "The Peppy Store"]:
                    continue

                url = pattern_final.split(' ')[0]
                book_price = ' '.join(pattern_final.split(' ')[1:3])
                book_price_used = re.sub(r' from', "", book_price)
                book_price_used = book_price_used.replace('used', '')
                book_price_plus = re.sub(r' +', "", book_price_used)
                book_price_plus = book_price_plus.replace('+', '')
                book_price_only = re.sub(r' used', "",book_price_plus)
                book_price_only = float(book_price_only.replace(',', ''))
                if float(book_price_only) < 500:
                    hyperlink_price = create_hyperlink(website_name, url, book_price_only)
                    # print(hyperlink_price, "\n\n")
                    price_list.append(hyperlink_price)
            # count +=1
            # if count ==10:
            #     break
        # print(len(prices))
        # price_len = len(prices)
        # return price_len

        # for div in soup.find_all('div', attrs={'class': 'book-details'}):
        #     for a in div.find_all('a'):
        #         a.extract()
        p_tags_without_class = soup.find_all('p', attrs={'class': 'book-description'})
        for p_tag in p_tags_without_class:
            if p_tag.find('a'):
                p_tag.find('a').extract()
        
    # print(price_list)
    return price_list

# for landing page
def index(request):
    allBooks = []
    category_books = Book.objects.values('category', 'book_id')
    # print("Category_books", category_books)
    cats = {item['category'] for item in category_books}
    # print("Cats", cats)

    for cat in cats:
        product = Book.objects.filter(category=cat)
           
        n = len(product)
        nSlides = n//6 + ceil((n/6) - (n//6))

        # productById = product.values_list('book_id')
        # fav = []
        # for i in range(len(productById)):
        #     if favouriteBook.objects.filter(book_id_db=productById[i], current_user=request.user).exists():
        #         fav.append(True)
        #     else:
        #         fav.append(False)
        # print(fav)
    
        allBooks.append([product, range(1, nSlides), nSlides])
        # print("Product", product)
        # print("productById", productById)
   
    # print("Allbooks", allBooks) 

    # print(fav)

    global params
    params={'allBooks':allBooks}
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
      messages.warning(request, 'Your message has been sent sucessfully!')
    return render(request, "bookReview/contact.html")


# for search page
def searchInput(request):
    # global searchInputText 
    # try:
    #     searchInputText = request.GET.get('arg')
    # except:
    #     searchInputText = ''
    # # return redirect('/?arg=%s' % searchInputText)
    # return render(request, "bookReview/index.html", params)
    pass

def search(request):
    # The API provides maximum 40 results -- search by booknames
    query = request.GET.get('text')
    searchInputText = request.GET.get('searchBy')
    print(">>>>>>>>>>>>",searchInputText)

    if searchInputText == 't':
        data = requests.get("https://www.googleapis.com/books/v1/volumes?q=intitle:" + query + "&printType=books&maxResults=36")

    elif searchInputText == 'a':
        data = requests.get("https://www.googleapis.com/books/v1/volumes?q=inauthor:" + query + "&printType=books&maxResults=36")

    elif searchInputText == 'i':
        data = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + query + "&printType=books&maxResults=36")

    else:
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
    y = specificBook(request, data=data)
    
    return render(request, "bookReview/details.html", y)


def specificBookDB(request, id):
    
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

    price_print = price(request)
    price_len = range(len(price_print))
    # print(price_len)
    # print(price_print)

    if request.user.is_authenticated:
        if favouriteBook.objects.filter(book_id_db=id, current_user=request.user).exists():
            fav = True
            # print(fav,title)
        else:
            fav = False
            # print(fav,title)
    else: 
        fav = None

    if UserReview.objects.filter(bookId=id).exists():
        val = UserReview.objects.filter(bookId=id).values()
        # print(val)

        review = []
        date = []
        username = []
        primary_key = []

        for i in range(len(val)):
            review.append(val[i]['reviewText'])
            date.append(val[i]['date'])
            current_user_id = val[i]['current_user_id']
            username.append((User.objects.get(id=current_user_id)).username)
            primary_key.append(val[i]['reviewId'])

        review_length = range(len(review))

    else:
        review = 0
        date = 0
        username = 0
        review_length = 0
        primary_key = 0

    display = {'title':title, 'author': author, 'publisher': publisher, 'publish_date': publish_date, 'no_pages': no_pages, 'image': image, 'desc': desc, 'isbn10': isbn10, 'isbn13': isbn13, 'title_for_url': title_for_url, 'title_for_bmarks': title_for_bmarks, 'book_id_db': id, 'price_print': price_print, 'price_len': price_len, 'fav': fav, 'review': review, 'date': date, 'username': username, 'review_length': review_length, 'primary_key': primary_key}
   
    return display

# for detailed view (Landing page)
def detailsHome(request):
    id = request.GET.get('bookId')
    x = specificBookDB(request, id)


    return render(request, "bookReview/detailsHome.html", x)


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(username=username, password=pwd)

        if user is not None:
            login(request, user)
            fname = user.first_name
            lname = user.last_name

            # messages.success(request, 'Logged In sucessfully!')
            # return render(request, "bookReview/login.html")
            return redirect('/userProfile/')
        
        else:
            messages.error(request, "Something is wrong, Please try again")
            return render(request, "bookReview/login.html")

    return render(request, "bookReview/login.html")

def signup(request):
    if request.method == "POST":
      # gets the details through 'name' attribute
        try:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')  
            username= request.POST.get('uname')  
            pwd = request.POST.get('pwd')
            pwd2 = request.POST.get('pwd2')
        
        #   user = UserSignup(first_name=first_name,last_name=last_name,username=username, email=email)
        #   user.save()

            if pwd != pwd2:
                messages.warning(request, "Password does not match")
            else:
                myuser = User.objects.create_user(username, email, pwd)
                myuser.first_name = fname
                myuser.last_name = lname
                myuser.save()
                
                messages.success(request, 'Your account has been created sucessfully!')
                return redirect('/signin/')
            
      
        except:
            messages.error(request, 'Something is wrong, Please try again')
            return redirect('/signup/')
    return render(request, "bookReview/signup.html")


def signout(request):
    logout(request)
    messages.info(request, "Keep on reading and don't forget to log back in for more!")
    # return redirect('signin')
    return render(request, "bookReview/login.html")

 
# for pagination -- wont work for previous and next buttons yet
# def pages(request, digit):
#     index = digit
#     for_totalItems = requests.get("https://www.googleapis.com/books/v1/volumes?q=subject:" + genre +"&printType=books")
#     returned_result = api(query=genre, data=for_totalItems)
#     totalItems = returned_result['results']

#     if index == -1:
#         i = request.GET.get('i')
#         # prev_index = i - 36                                                                                                                                                                              
#     if index == 1:
#         startIndex = "36"
#         # print("index=1")
#     elif index == 2:
#         startIndex = "73"
#         # print("index=2")

#     elif index == 3:
#         startIndex = "109"
#         # print("index 3")

#     data = requests.get("https://www.googleapis.com/books/v1/volumes?q=subject:" + genre + "&startIndex=" + startIndex +"&printType=books&maxResults=36")
#     x = api(query=genre, data=data)
#     return render(request, "bookReview/page.html", x)


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

        # print(new_soup)
        # print(name_text)

        review_span = [span.text for span in s1]
        # print("review-span: ", review_span)  
        if review_span:
            review_span.pop(0)
        # length = [len(i) for i in review_span]
        short_reviews = []
        reviewer = []
        msg = "No reviews found at the moment, Please try again by refreshing the page!"
        for i in range(len(review_span)):
            if len(review_span[i]) <= 2000:
                reviewer.append(name_text[i])
                short_reviews.append(review_span[i])
                msg = ""

        # print(">>>>>>", short_reviews)
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
    # print("msg: ", msg)
    return render(request, "bookReview/reviews.html", {'test':test, 'title_GR': title_GR, 'goodreads': goodreads, 'short_reviews': short_reviews, 'spans_length': spans_length, 'reviewer': reviewer, 'msg': msg, 'flag': flag})


# ------------------------------ FAVOURITES --------------------------------

def fav_details(request):
    fav_list = favouriteBook.objects.filter(current_user=request.user)
    api_book_list = fav_list.filter(book_from_api=True)
    db_book_list = fav_list.filter(book_from_api=False)
    api_book_list = fav_list.filter(book_from_api=True)
    db_book_list = fav_list.filter(book_from_api=False)

    api_books = []
   
    for i in range(len(api_book_list)):
        data = requests.get("https://www.googleapis.com/books/v1/volumes/" + api_book_list[i].book_id_api)
        y = specificBook(request, data=data)
        api_books.append(y)

    api_books.extend(db_book_list)
    # print(api_books)
    return api_books


def favourites(request):
    
    if request.user.is_authenticated:
        user = request.user
        firstname = request.user.get_short_name()
        fullname = request.user.get_full_name()
        
        if request.POST:
            hidden_bookId = request.POST['hidden_bookId']

            if hidden_bookId.isnumeric() == True:
                book_from_api = False
                book_id_db = Book.objects.get(book_id=hidden_bookId)
                book_id_api = None
                # print(book_id_db)
            
            else:
                book_id_db = None
                book_id_api = hidden_bookId
                book_from_api =  True
                # print(book_id_api)

            try:
                favBook = favouriteBook(current_user=request.user, book_id_db=book_id_db, book_id_api=book_id_api, book_from_api=book_from_api)
                favBook.save()
                messages.warning(request, 'Added to Favourites!')
                x = fav_details(request)

                return render(request, "bookReview/userProfile.html", {"books": x, 'user': user, 'firstname': firstname, 'fullname': fullname})
            
            except:
                messages.warning(request, 'Book already added to favourites !')
                x = fav_details(request)
                return render(request, "bookReview/userProfile.html", {"books": x, 'user': user, 'firstname': firstname, 'fullname': fullname})
                
            # print(">>>>>>>>>",  hidden_bookId)
    else:
        return redirect('/signin/')
    
    x = fav_details(request)
    # print(x)

    return render(request, "bookReview/userProfile.html",{"books": x, 'user': user, 'firstname': firstname, 'fullname': fullname})


def favDelete(request):
    user = request.user
    firstname = request.user.get_short_name()
    fullname = request.user.get_full_name()

    if request.user.is_authenticated:
        if request.POST:
            hidden_bookId = request.POST['hidden_bookId']

            if hidden_bookId.isnumeric() == True:
                favouriteBook.objects.filter(book_id_db=hidden_bookId).delete()
                
            
            else:
                favouriteBook.objects.filter(book_id_api=hidden_bookId).delete()

                
    x = fav_details(request)
    return render(request, "bookReview/userProfile.html",{"books": x, 'user': user, 'firstname': firstname, 'fullname': fullname})


def userReview(request):
    if request.user.is_authenticated:
        if request.POST:
            id = request.GET.get('id')
            reviewText = request.POST.get('message')
            userReview = UserReview(current_user=request.user, bookId=id, reviewText=reviewText)
            userReview.save()

            if id.isnumeric():
                x = specificBookDB(request, id)
                return render(request, "bookReview/detailsHome.html", x)
            else:
                data = requests.get("https://www.googleapis.com/books/v1/volumes/" + id)
                x = specificBook(request, data=data)
                return render(request, "bookReview/details.html", x)
            


def ReviewDelete(request):
    if request.user.is_authenticated:
        if request.POST:
            id = request.GET.get('id')

            pk = request.POST['primary_key']
            # print(">>>>>>>", pk)
            UserReview.objects.filter(reviewId=pk, current_user=request.user).delete()

            if id.isnumeric():
                x = specificBookDB(request, id)
                return render(request, "bookReview/detailsHome.html", x)
            else:
                data = requests.get("https://www.googleapis.com/books/v1/volumes/" + id)
                x = specificBook(request, data=data)
                return render(request, "bookReview/details.html", x)
            

def rules(request):
    return render(request, "bookReview/rules.html")

def policies(request):
    return render(request, "bookReview/policies.html")

def terms(request):
    return render(request, "bookReview/terms.html")
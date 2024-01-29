from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Book, Author, Borrow, UserProfile
from django.db.models import Q

# landing page
def index(request):
    return render(request, 'index.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('/signin/')
    else:
        return render(request, 'signup.html')
  

# sign in page and its subpages=============================================================
def signin_view(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_rememberme = request.POST.get('user_rememberme')
        staff_username = request.POST.get('staff_username')
        staff_password = request.POST.get('staff_password')
        staff_rememeberme = request.POST.get('staff_rememberme')

        if username and password and username != None and password != None:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                request.session['username'] = username # Store username in session
                if user_rememberme:
                    request.session['password'] = password
                return redirect('/user_menu/')
            else:
                context['error_user'] = 'Invalid username or password.'
            
        elif staff_username and staff_password and staff_username != None and staff_password != None:
            staff = authenticate(request, username=staff_username, password=staff_password)
            
            if staff is not None:
                login(request, staff)
                request.session['staff_username'] = staff_username  # Store staff_username in session
                if staff_rememeberme:
                    request.session['staff_password'] = staff_password
                return redirect('/staff_menu/')
            else:
                context['error_staff'] = "Invalid staff username or password"
        else:
            context['input_error'] = "Please enter username and password"
    # Default response for GET requests and unsuccessful POST requests
    return render(request, 'signin.html', context)

def forgot_pwd_view(request):
    return render(request, 'forgot_pwd.html')
# ==========================================================================================


# staff menu and its subpages=============================================================== 
def staff_view(request):
    staff_username = request.session.get('staff_username')
    return render(request, 'staff_menu.html', {'name': staff_username})
    

def create_book_view(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        book_title = request.POST['title']
        book_author = Author.objects.get(id=int(request.POST['author']))
        book_price = request.POST['price']
        book_stock = request.POST['stock']
        book_publisher = request.POST['publisher']
        Book.create_book(book_title, book_author, book_price, book_stock, book_publisher)
        return HttpResponse("book created")
    else:
        return render(request, 'create_book.html', {'authors': authors})


def create_author_view(request):
    staff_username = request.session.get('staff_username')
    if request.method == 'POST':
        author_name = request.POST['name']
        Author.objects.create(name=author_name)
        return
    return render(request, 'create_author.html', {'name': staff_username})


def user_management_view(request):
    return render(request, 'user_management.html')
# ==========================================================================================


# user menu and its subpages================================================================
def user_menu_view(request):
    books = Book.objects.all()
    if request.method == 'POST':
        # get books from database
        title_query = request.GET.get('title', '')
        author_query = request.GET.get('author', '')
        publisher_query = request.GET.get('publisher', '')
        
        books = Book.objects.filter(
            Q(title__icontains=title_query) &
            Q(author__name__icontains=author_query) &
            Q(publisher__icontains=publisher_query)
        )
        
        # check if books are available
        books = book_ava_stocks(books)
        
        # Get the book the user wants to borrow
        book_id = request.POST.get('book_id')
        amount = int(request.POST.get('amount'))
        book = Book.objects.get(id=book_id)

        # Get the current user
        temp_username = request.session.get('username')
        user = User.objects.get(username=temp_username)

        # Check if a UserProfile already exists for this user
        if not UserProfile.objects.filter(user=user).exists():
            # If not, create a new UserProfile object
            UserProfile.objects.create(user=user)

        # Get the UserProfile for the current user
        user_profile = UserProfile.objects.get(user=user)


        # Create a new Borrow object
        Borrow.create_borrow(user_profile, book)
        
        # make necessary changes to the book table
        Book.borrow_book(book, amount)
        
    return render(request, 'user_menu.html', {'books': books})

def my_books_view(request):
    temp_username = request.session.get('username')
    user = User.objects.get(username=temp_username)
    borrowed_books = UserProfile.get_borrowed_books(user)
    return render(request, 'my_books.html', {'books': borrowed_books})

def check_out_view(request):
    return render(request, 'check_out.html')

def book_ava_stocks(books):
    for book in books:
        if book.stock <= 0:
            #remove from books list
            books.remove(book)
    return books
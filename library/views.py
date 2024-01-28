from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Book, Author
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
  


def signin_view(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        staff_username = request.POST.get('staff_username')
        staff_password = request.POST.get('staff_password')

        if username and password and username != None and password != None:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/user_menu/')
            else:
                context['error_user'] = 'Invalid username or password.'
            
        elif staff_username and staff_password and staff_username != None and staff_password != None:
            staff = authenticate(request, username=staff_username, password=staff_password)
            
            if staff is not None:
                login(request, staff)
                request.session['staff_username'] = staff_username  # Store staff_username in session
                return redirect('/staff_menu/')
            else:
                context['error_staff'] = "Invalid staff username or password"
        else:
            context['input_error'] = "Please enter username and password"
    # Default response for GET requests and unsuccessful POST requests
    return render(request, 'signin.html', context)

  
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
        return render(request, 'staff_menu.html', {'authors': authors})

def create_author_view(request):
    if request.method == 'POST':
        author_name = request.POST['name']
        Author.objects.create(name=author_name)
        return 
    return render(request, 'staff_menu.html')

def user_management_view(request):
    return render(request, 'user_management.html')


def forgot_pwd_view(request):
    return render(request, 'forgot_pwd.html')

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
            Q(publisher__name__icontains=publisher_query)
        )
        
        # check if books are available
        books = book_ava_stocks(books)
        
    return render(request, 'user_menu.html', {'books': books})

def check_out
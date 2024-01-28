# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db import models

# author table
class Author(models.Model):
    name = models.CharField(max_length=200)
    
# transaction table
class Transaction(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)

# book table
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    publisher = models.CharField(max_length=200, default="Null")

    @classmethod
    def create_book(cls, title, author, price, stock, publisher):
        book = cls(title=title, author=author, price=price, stock=stock, publisher=publisher)
        book.save()

    @classmethod
    def borrow_book(self, amount):
        if self.stock < amount:
            raise ValueError('Not enough stock')
        else:
            self.stock -= amount
            self.save()
    
    @classmethod
    def return_book(self, amount):
        self.stock += amount
        self.save()       
        
# user profile table
# it's a one-to-one relationship with the built in User table of django
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    borrowed_books = models.ManyToManyField(Book, through='Borrow')
    
    @classmethod
    def get_borrowed_books(user):
        user_profile = UserProfile.objects.get(user=user)
        borrowed_books = user_profile.borrowed_books.all()
        return borrowed_books

# borrow table
class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
# Create your models here.
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    

class Transaction(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)

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
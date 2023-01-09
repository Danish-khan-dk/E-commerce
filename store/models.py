from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(s):
        return s.name

class Brands(models.Model):
    brand = models.CharField(max_length=200)

    def __str__(s):
        return s.brand

class Filter_Price(models.Model):
    Filter_Price = (
        ('0 TO 500', '500 TO 1000'),
        ('500 TO 1000', '1000 TO 1500'),
        ('1000 TO 1500', '1500 TO 2000'),
        ('1500 TO 2000', '2000 TO 2500'),
    )

    price = models.CharField(choices=Filter_Price, max_length=60)

    def __str__(s):
        return s.price

class Product(models.Model):
    image = models.ImageField(upload_to="media/products/")
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    filter_Price = models.ForeignKey(Filter_Price,on_delete=models.CASCADE,default=0)
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE,default=0)
    brands = models.ForeignKey(Brands,on_delete=models.CASCADE,default=0)

    def __str__(s):
        return s.name


class Images(models.Model):
    image = models.ImageField(upload_to="media/products/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Contact_us(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(s):
        return s.email

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/Order_Img')
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=10000)

    def __str__(self):
        return self.order.user.username
from datetime import datetime
from distutils import text_file
from distutils.command.upload import upload
from email.mime import image
from email.policy import default
from pyexpat import model
from sqlite3 import Timestamp
from unicodedata import category
from django.db import models

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50,default='')
    category=models.CharField(max_length=50,default='')
    sub_category=models.CharField(max_length=50,default='')
    price=models.IntegerField(default='0')
    description= models.CharField(max_length=500)
    published_date = models.DateField()
    image=models.ImageField(upload_to='shop/images',default='')
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    phone=models.CharField(max_length=50,default='')
    email= models.EmailField(max_length=50,default='')
    desc= models.CharField(max_length=50000,default='')


    def __str__(self):
        return self.name

class Order(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    zip_code=models.CharField(max_length=50)
    phone=models.CharField(max_length=10,default='')

    def __str__(self):
        return self.email

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id=models.IntegerField(default='')
    update_desc= models.CharField(max_length=10000)
    timestamp= models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + '....'
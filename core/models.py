
from datetime import datetime
from statistics import quantiles
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
import math

class Tag(models.Model):
  name = models.CharField(max_length=40)

  def __str__(self):
      return self.name

class Category(models.Model):
  name = models.CharField(max_length=40)

  class Meta:
    ordering = ("name",)
    verbose_name = "category"
    verbose_name_plural = "categories"


  def __str__(self):
    return self.name

class Product(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    adress = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, db_index=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    description = models.TextField(max_length=200)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    shelf_life = models.DateField()
    image = models.ImageField(upload_to='', null=True)
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, max_length=60, on_delete=models.CASCADE, blank=False, default="Other", null=False)
    tags = models.ManyToManyField(Tag, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)


    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    

    def time_left(self):
        now = datetime.now().date()
        
        diff= self.shelf_life - now

        
        if diff.days == 0 and diff.seconds >= 0:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour left"

            else:
                return str(hours) + " hours left"

        if diff.days >= 1:
            days = diff.days
        
            if days == 1:
                return str(days) + " day left"

            else:
                return str(days) + " days left"

        else:
            days = diff.days
            if days == 1:
                return "Overdue " + str(-days) + " day"

            else:
                return "Overdue " + str(-days) + " days"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, db_index=True)
    products = models.ManyToManyField(Product, blank=True)
    slug = models.SlugField(max_length=200, db_index=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.slug)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    
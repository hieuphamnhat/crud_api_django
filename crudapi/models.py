from django.db import models

# Create your models here.
class Company(models.Model):
    symbol = models.CharField(max_length=50)
    price = models.FloatField(null=True)
    date = models.DateField(null=True)

#relationships

#1. many-to-many
class Publication(models.Model):
    title = models.CharField(max_length=30)
    
    def __str__(self):
        return self.title

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publication = models.ManyToManyField(Publication)
    
    def __str__(self):
        return self.headline

class Person(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name
class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')
 
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

#2. Many-to-one
class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Reports(models.Model):
    headline = models.CharField(max_length=100)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    def __str__(self):
        return "%s the place" % self.name

class Restaurant(models.Model):
    place = models.OneToOneField(
        Place, 
        on_delete=models.CASCADE,
        primary_key=True)
    hot_dogs = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name

class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant,
    on_delete = models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)
        
    

    
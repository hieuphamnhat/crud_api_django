from django.db import models

# Create your models here.
class Company(models.Model):
    symbol = models.CharField(max_length=50)
    price = models.FloatField(null=True)
    date = models.DateField(null=True)

#relationships
#many-to-many
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
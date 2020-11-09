from django.db import models

# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Dress(models.Model):
    """Класс одежда. Через ключ ForeignKey привязан к человеку.
    Организована связь один человек много одежды"""
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Chaild(models.Model):
    """Класс ребенок. Через ключ ManyToManyField привязан к родителю.
    Организована связь много детей к многим родителям"""
    person = models.ManyToManyField(Person)


class Blog(models.Model):
    """ """
    name = models.CharField(max_length=155)
    tagline = models.TextField()


class Author(models.Model):
    """  """
    name = models.CharField(max_length=200)
    email = models.EmailField()


class Entry(models.Model):
    """ """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)


class Category(models.Model):
    title = models.CharField(max_length=255)


class Topic (models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    categories = models.ManyToManyField(Category, related_name='topics')

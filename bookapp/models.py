from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.IntegerField()
    image = models.ImageField()
    title = models.TextField()
    summary = models.TextField()

class Paragraph(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, related_name='book')
    para_id = models.IntegerField()
    content = models.TextField()
    sentence = models.TextField()
    image = models.ImageField()
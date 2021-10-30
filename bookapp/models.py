from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.IntegerField(null=False, primary_key=True)
    image = models.ImageField(upload_to='books/', null=False)
    title = models.TextField(null=False)
    summary = models.TextField(null=False)

class Paragraph(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book', db_column='book_id')
    para_id = models.IntegerField(null=False)
    content = models.TextField(null=False)
    sentence = models.TextField(null=False)
    image = models.ImageField(upload_to='dalle/', null=False)
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from bookapp.models import Book, Paragraph


class MainView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'bookapp/main.html'
    paginate_by = 6


class BookView(DetailView):
    model = Book
    context_object_name = 'target_book'
    template_name = 'bookapp/book.html'

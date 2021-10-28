from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from bookapp.models import Book, Paragraph


class MainView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'bookapp/main.html'
    # paginate_by = 6


class BookView(DetailView):
    model = Book
    context_object_name = 'target_book'
    template_name = 'bookapp/book.html'

    def get_context_data(self, **kwargs):
        book_list = Book.objects.filter(book_id=self.book_pk)
        para_pk = self.para_pk
        return super().get_context_data(book_list=book_list, para_pk=para_pk, **kwargs)
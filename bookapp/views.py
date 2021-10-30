from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from bookapp.models import Book, Paragraph


class MainView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'bookapp/main.html'
    # paginate_by = 6


def BookView(request, book_pk, para_pk):
    para_list = Paragraph.objects.filter(book_id=book_pk)
    max = para_list.count()

    if para_pk == 1:
        prev_pk = 0
    else:
        prev_pk = para_pk - 1
    if para_pk == max:
        next_pk = 0
    else:
        next_pk = para_pk + 1

    context = {
        'para_list': para_list,
        'para_pk': para_pk,
        'prev_pk': prev_pk,
        'next_pk': next_pk
    }

    return render(request, 'bookapp/book.html', context)


# class BookView(DetailView):
#     model = Book
#     context_object_name = 'target_book'
#     template_name = 'bookapp/book.html'
#
#     def get_context_data(self, **kwargs):
#         para_list = Paragraph.objects.filter(book_id=self.pk)
#         max = para_list.count()
#         para_pk = self.para_pk
#         if para_pk == 1:
#             prev_pk = 0
#         else:
#             prev_pk = para_pk - 1
#         if para_pk == max:
#             next_pk = 0
#         else:
#             next_pk = para_pk + 1
#         return super().get_context_data(para_list=para_list, para_pk=para_pk, prev_pk=prev_pk, next_pk=next_pk, **kwargs)
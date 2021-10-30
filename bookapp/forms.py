from django.forms import ModelForm

from bookapp.models import Book, Paragraph


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['image', 'title', 'summary']


class ParagraphForm(ModelForm):
    class Meta:
        model = Paragraph
        fields = ['book', 'para_id', 'content', 'sentence']
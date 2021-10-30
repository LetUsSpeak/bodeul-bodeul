import requests
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView

from bookapp.forms import BookForm, ParagraphForm
from bookapp.models import Book, Paragraph


class MainView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'bookapp/main.html'


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


def BookCreateView(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # book = form.save(commit=False)
            form.save()
            return redirect('para_create')
    else:
        form = BookForm()
        return render(request, 'bookapp/create_book.html', {'form': form})


def ParagraphCreateView(request):
    if request.method == 'POST':
        form = ParagraphForm(request.POST)
        if form.is_valid():
            paragraph = form.save(commit=False)
            sentence = form.cleaned_data['sentence']
            eng_sentence = papago(sentence)
            paragraph.image = dall_e(eng_sentence)[0]
            paragraph.save()

            content = form.cleaned_data['content']
            book_id = paragraph.book_id
            para_id = form.cleaned_data['para_id']
            make_audio(content, book_id, para_id)

            return redirect('main')
    else:
        form = ParagraphForm()
        return render(request, 'bookapp/create_paragraph.html', {'form': form})


def papago(text):
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
        'X-Naver-Client-Id': 'brfL28fIiSDPXYs0mias',
        'X-Naver-Client-Secret': 'QFImDfwoR0'
    }
    data = {
        'source': 'ko',
        'target': 'en',
        'text': text

    }
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    return result['message']['result']['translatedText']


def dall_e(eng_text):
    url = 'https://main-dalle-server-scy6500.endpoint.ainize.ai/generate'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = '{"text": "%s", "num_images": 1}' % eng_text
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    return result


def make_audio(text, book_id, para_id): # 여기 인자 받아서 저장되는 이름 바꾸기
    url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    key = '43fdc9455b281f774ea7f7c850fa57ba'
    headers = {
        "Content-Type": "application/xml",
        "Authorization": "KakaoAK " + key,
    }
    data = f'<speak> \
    <voice name="WOMAN_READ_CALM"> \
    <prosody rate="slow" volume="loud">{text}</prosody> \
    </voice></speak>'.encode('utf-8')
    res = requests.post(url, headers=headers, data=data)
    with open(f"static/tts_file/{book_id}_{para_id}.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(res.content)
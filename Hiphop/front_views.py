from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def tagger(request):
    return render(request, 'tagger.html')

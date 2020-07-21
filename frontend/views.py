from django.shortcuts import render


def login(request):
    return render(request, 'signIn.html')

def registration(request):
    return render(request, 'signUp.html')

def artcileList(request):
    return render(request, 'index.html')

def article(request, article_id):
    return render(request, 'article.html', {'article_id': article_id})

def addnew(request):
    return render(request, 'addArticle.html')
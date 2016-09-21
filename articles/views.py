from django.shortcuts import render, HttpResponse, Http404

from .models import Entry
from django.contrib.auth.decorators import login_required
from users.models import MyUser

@login_required(None,None,'/login')
def articles_list(request):

    articles = Entry.objects.published().order_by('-created_at').all()

    return render(request,'blog.html',{
        'sa':'Smolyar Andriy',
        'articles' : articles
    })
@login_required(None,None,'/login')
def article(request,id):

    article = Entry.objects.published().filter(id=id).first()
    if article == None:
        raise Http404('Page not Found')

    return render(request,'article.html',{
        'article' : article
    })



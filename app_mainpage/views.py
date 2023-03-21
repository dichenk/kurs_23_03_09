from django.shortcuts import render
from app_blog.models import Blog_Article
from app_spammy.models import Client, Newsletter
import random as rnd


def mainpagew(request):
    template = 'app_mainpage/index.html'
    article_list = Blog_Article.objects.all().order_by('?')[:3]
    client_list = Client.objects.all()
    maillist_list = Newsletter.objects.all()
    maillist_active = Newsletter.objects.filter(mailing_status='launched')

    pass_to_template = {
        'item': article_list,
        'client': client_list,
        'maillist': maillist_list,
        'maillist_active': maillist_active,
    }
    return render(request, template, pass_to_template)

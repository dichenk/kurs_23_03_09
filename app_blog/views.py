# from django.shortcuts import redirect  # import render, get_object_or_404,
from django.shortcuts import render

from app_blog.models import Blog_Article
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django import template
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from app_users.models import Users


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Blog_Article
    fields = ('article_head', 'article_body', 'image')
    success_url = reverse_lazy('app_blog:blog_list')
    template_name = 'app_blog/blog_create.html'

    def get_queryset(self):
        return User.objects.filter().include(groups__name='manager')


class ArticleListView(ListView):
    model = Blog_Article
    template_name = 'app_blog/blog_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Blog_Article.objects.filter(author=self.request.user)


class ArticleDetailView(DetailView):
    model = Blog_Article
    template_name = 'app_blog/blog_detail.html'

    def get_object(self):
        obj = super().get_object()
        obj.num_of_views += 1
        obj.save()
        # context = self.get_context_data(object=self.object)
        return obj


class ArticleDeleteView(DeleteView):
    model = Blog_Article
    success_url = reverse_lazy('app_blog:blog_list')
    template_name = 'app_blog/blog_delete.html'

    def get_queryset(self):
        return Blog_Article.objects.filter(author=self.request.user)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog_Article
    fields = ('article_head', 'article_body', 'image')
    template_name = 'app_blog/blog_update.html'
    success_url = reverse_lazy('app_blog:blog_list')


    def get_queryset(self):
        return Blog_Article.objects.filter(author=self.request.user)
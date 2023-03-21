from django.urls import path
from config import settings
from app_blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from django.conf.urls.static import static

app_name = 'app_blog'


urlpatterns = [
    path('create', ArticleCreateView.as_view(), name='blog_create'),
    path('list', ArticleListView.as_view(), name='blog_list'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='blog_detail'),
    path('update/<int:pk>', ArticleUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name='blog_delete'),
]


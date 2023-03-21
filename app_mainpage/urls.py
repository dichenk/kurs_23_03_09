from django.urls import path
from config import settings
from django.conf.urls.static import static
from app_mainpage.views import mainpagew

app_name = 'app_mainpage'

urlpatterns =[
path('', mainpagew, name='main')
]

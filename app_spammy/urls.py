from django.urls import path
from config import settings
from app_spammy.views import ClientListView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, NewsletterListView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView, MessageToSendListView, MessageToSendCreateView, \
    MessageToSendUpdateView, MessageToSendDeleteView, change_status, change_status_super
# , , AttemptToSendListView, , , , ,
from django.conf.urls.static import static

app_name = 'app_spammy'

urlpatterns = [
    path('clients', ClientListView.as_view(), name='client_list'),
    path('create_client', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),

    path('newsletter', NewsletterListView.as_view(), name='newsletter_list'),
    path('create_newsletter', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('update_newsletter/<int:pk>', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('delete_newsletter/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),

    path('mail', MessageToSendListView.as_view(), name='mail_list'),
    path('create_mail', MessageToSendCreateView.as_view(), name='create_mail'),
    path('update_mail/<int:pk>', MessageToSendUpdateView.as_view(), name='update_mail'),
    path('delete_mail/<int:pk>', MessageToSendDeleteView.as_view(), name='delete_mail'),

    # path('maillistlog', AttemptToSendListView.as_view(), name='maillistlog'),



    path('status/<int:pk>/', change_status, name='status'),
    path('status_super/<int:pk>/', change_status_super, name='status_super'),

]
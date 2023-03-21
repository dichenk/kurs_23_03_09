from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from app_spammy.models import Client, Newsletter, MessageToSend
# , , AttemptToSend
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from app_users.models import Users


class ClientListView(ListView):
    model = Client
    template_name = 'app_spammy/client_list.html'
    paginate_by = 2
    def get_queryset(self):
        return Client.objects.filter(author=self.request.user).order_by('pk')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('email', 'name', 'comment')
    success_url = reverse_lazy('app_spammy:client_list')
    template_name = 'app_spammy/client_create.html'

    def get(self, request):
        if self.request.user.groups.filter(name='news_author').exists():
            return super().get(self, request)
        else:
            raise Http404("У вас недостаточно прав!")

    # def get_queryset(self):
    #     if self.request.user.groups.filter(name='banned').exists():
    #         raise Http404("You are banned!")
    #     return super().get_queryset()


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('email', 'name', 'comment')
    template_name = 'app_spammy/client_update.html'
    success_url = reverse_lazy('app_spammy:client_list')

    def get_queryset(self):
        return Client.objects.filter(author=self.request.user)


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('app_spammy:client_list')
    template_name = 'app_spammy/client_delete.html'

    def get_queryset(self):
        # if self.request.user.groups.filter(name='banned').exists():
        #     raise Http404("You are banned!")
        return Client.objects.filter(author=self.request.user)


class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'newsletter_list.html'
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return Newsletter.objects.order_by('pk')
        else:
            return Newsletter.objects.filter(author=self.request.user).order_by('pk')




class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    fields = ('name_of', 'comment', 'client', 'posting_date', 'posting_time', 'frequency')
    success_url = reverse_lazy('app_spammy:newsletter_list')
    template_name = 'app_spammy/newsletter_create.html'

    def get(self, request):
        if self.request.user.groups.filter(name='news_author').exists():
            return super().get(self, request)
        else:
            raise Http404("У вас недостаточно прав!")


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    fields = ('name_of', 'comment', 'client', 'posting_date', 'posting_time', 'frequency')
    success_url = reverse_lazy('app_spammy:newsletter_list')
    template_name = 'app_spammy/newsletter_update.html'

    def get_queryset(self):
        return Newsletter.objects.filter(author=self.request.user)


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('app_spammy:newsletter_list')
    template_name = 'app_spammy/newsletter_delete.html'

    def get_queryset(self):
        return Newsletter.objects.filter(author=self.request.user)


class MessageToSendListView(ListView):
    model = MessageToSend
    template_name = 'app_spammy/mail_list.html'
    paginate_by = 2

    def get_queryset(self):
        return MessageToSend.objects.filter(author=self.request.user).order_by('pk')


class MessageToSendCreateView(LoginRequiredMixin, CreateView):
    model = MessageToSend
    fields = ('name_of', 'comment', 'newsletter', 'letter_subject', 'body_of_the_letter')
    success_url = reverse_lazy('app_spammy:mail_list')
    template_name = 'app_spammy/mail_create.html'

    def get(self, request):
        if self.request.user.groups.filter(name='news_author').exists():
            return super().get(self, request)
        else:
            raise Http404("У вас недостаточно прав!")


class MessageToSendUpdateView(LoginRequiredMixin, UpdateView):
    model = MessageToSend
    fields = ('name_of', 'comment', 'newsletter', 'letter_subject', 'body_of_the_letter')
    success_url = reverse_lazy('app_spammy:mail_list')
    template_name = 'app_spammy/mail_update.html'

    def get_queryset(self):
        return MessageToSend.objects.filter(author=self.request.user)


class MessageToSendDeleteView(DeleteView):
    model = MessageToSend
    success_url = reverse_lazy('app_spammy:mail_list')
    template_name = 'app_spammy/mail_delete.html'

    def get_queryset(self):
        return MessageToSend.objects.filter(author=self.request.user)



# class AttemptToSendListView(ListView):
#     model = AttemptToSend


def change_status(request, pk):
    maillist_item = get_object_or_404(Newsletter, pk=pk)
    if maillist_item.mailing_status == 'created' and maillist_item.author==request.user:
        if hasattr(maillist_item, 'messagetosend'):
            start_mailing(maillist_item)
            maillist_item.mailing_status = 'launched'
        else:
            raise Http404("Чтобы запустить рассылку, вам нужно создать письмо")
    elif maillist_item.mailing_status == 'launched' and maillist_item.author==request.user:
        maillist_item.mailing_status = 'created'
    else:
        raise Http404("Только автор рассылки может запустить (остановить) рассылку")
    maillist_item.save()
    return redirect(reverse_lazy('app_spammy:newsletter_list'))

def change_status_super(request, pk):
    maillist_item = get_object_or_404(Newsletter, pk=pk)
    if (maillist_item.mailing_status == 'created' or maillist_item.mailing_status == 'launched') and request.user.groups.filter(name='manager').exists():
        maillist_item.mailing_status = 'disabled'
    else:
        raise Http404("Только менеджер может заблокировать рассылку")
    maillist_item.save()
    return redirect(reverse_lazy('app_spammy:newsletter_list'))


def start_mailing(maillist_item):
    mailru = maillist_item.messagetosend
    mail_subject = mailru.letter_subject
    message = mailru.body_of_the_letter
    mails = []
    for emailto in maillist_item.client.all():
        mails.append(emailto.email)
    email = EmailMessage(mail_subject, message, to=mails)  #[new_user.email])
    email.send()


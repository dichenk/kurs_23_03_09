from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView
from app_users.models import Users
from django.urls import reverse_lazy
from app_users.forms import UsersCreationForm
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from config import settings
from app_users.tokens import account_activation_token
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.http import Http404



# Create your views here.
class UsersLoginView(LoginView):
    model = Users
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('app_mainpage:main')


class UsersCreateView(CreateView):
    model = Users
    form_class = UsersCreationForm
    success_url = reverse_lazy('app_users:login')
    template_name = 'app_users/create.html'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            activate_email(self.object)
        return super().form_valid(form)


def activate_email(new_user):
    new_user.is_active = False
    mail_subject = 'Activate your user account.'
    message = render_to_string('app_users/activate_account.html', {
        'user': new_user.username,
        'domain': settings.BASE_URL,
        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
        'token': account_activation_token.make_token(new_user),
        'protocol': 'http'
    })
    email = EmailMessage(mail_subject, message, to=[new_user.email])
    email.send()


def activate(request, uidb64, token):
    Userr = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Userr.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Userr.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        group = Group.objects.get(name='news_author')
        user.groups.add(group)
        return redirect('app_users:login')


    return redirect('app_mainpage:main')


class ManagersUserListView(ListView):
    model = Users
    template_name = 'user_list.html'
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            return Users.objects.filter(groups__name__in=['news_author'])


def change_user_status(request, pk):
    users_item = get_object_or_404(Users, pk=pk)
    if users_item.groups.filter(name='news_author').exists():
        if users_item.groups.filter(name='manager').exists():
            raise Http404("Только superuser может заблокировать manager")
        else:
            g = Group.objects.get(name='banned')
            g.user_set.add(users_item)
            g = Group.objects.get(name='news_author')
            g.user_set.remove(users_item)
    return redirect(reverse_lazy('app_users:users'))
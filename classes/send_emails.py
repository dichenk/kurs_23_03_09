from django.core.mail import EmailMessage

def test_mail():
    email = EmailMessage('test', 'testtest', to=['dchenk@gmail.com'])  #[new_user.email])
    email.send()
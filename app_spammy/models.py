from django.db import models
from author.decorators import with_author

@with_author
class Client(models.Model):
    email = models.EmailField(
        blank=False,
        max_length=100,
        verbose_name='Электронная почта'
    )
    name = models.CharField(
        max_length=150,
        verbose_name='ФИО',
        default=None,
        blank=False
    )
    comment = models.TextField(verbose_name='Комментарий', default='Type here')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.email}\n'

@with_author
class Newsletter(models.Model):
    FREQUENCYS = (
        ('once a day', 'раз в день'),
        ('once a week', 'раз в неделю'),
        ('once a month', 'раз в месяц')
    )
    STATUSES = (
        ('completed,', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена'),
        ('disabled', 'выключена')
    )
    name_of = models.CharField(
        max_length=150,
        verbose_name='Наименование рассылки',
        default=None,
        blank=False
    )
    comment = models.TextField(verbose_name='Комментарий', default='')
    client = models.ManyToManyField(
        Client,
        verbose_name='Адресат',
    )
    posting_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Когда',
        default='2023-12-29'
    )
    posting_time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Во сколько',
        default='00:01'
    )
    frequency = models.CharField(choices=FREQUENCYS, default='once a day', max_length=20)
    mailing_status = models.CharField(choices=STATUSES, default='created', max_length=20)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.name_of}\n{self.comment}\n{self.mailing_status}\n'

@with_author
class MessageToSend(models.Model):
    name_of = models.CharField(
        max_length=150,
        verbose_name='Наименование письма',
        default=None,
        blank=False
    )
    comment = models.TextField(verbose_name='Комментарий', default='')
    newsletter = models.OneToOneField(
        Newsletter,
        verbose_name='Рассылка',
        on_delete=models.CASCADE,
        null=True
    )
    letter_subject = models.CharField(
        blank=True,
        max_length=100,
        verbose_name='Тема письма',
        default=None,
    )
    body_of_the_letter = models.TextField(
        blank=True,
        max_length=1000,
        verbose_name='Тело письма',
        default=None,
    )

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщение для рассылок'

    def __str__(self):
        return f'{self.name_of}\n{self.letter_subject}\n'

#
# class AttemptToSend(models.Model):
#
#     date_of_last_attempt = models.CharField(max_length=100, verbose_name='Дата последней попытки', default=None)
#     time_of_last_attempt = models.CharField(max_length=150, verbose_name='Время последней попытки', default=None)
#     attempt_status = models.CharField(max_length=150, verbose_name='Статус попытки', default=None)
#     mail_server_response = models.TextField(verbose_name='Ответ сервера', default=None)
#
#     class Meta:
#         verbose_name = 'Попытка рассылки'
#         verbose_name_plural = 'Попытки рассылок'
#
#     def __str__(self):
#         return f'{self.date_of_last_attempt}\n{self.mail_server_response}\n'
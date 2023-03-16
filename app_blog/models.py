from django.db import models
from author.decorators import with_author

@with_author
class Blog_Article(models.Model):
    article_head = models.CharField(
        blank=True,
        max_length=100,
        verbose_name='Заголовок',
        default=None,
    )
    article_body = models.TextField(
        blank=True,
        max_length=1000,
        verbose_name='Содержимое',
        default=None,
    )
    date_create = models.DateField('Дата создания', auto_now_add=True, null=True)
    date_last_change = models.DateField('Дата обновления', auto_now=True, null=True)
    image = models.ImageField('Изображение', upload_to='blog/', blank=True)
    num_of_views = models.PositiveIntegerField('Счетчик просмотров', default=0)


    class Meta:
        verbose_name = 'Статья в блоке'
        verbose_name_plural = 'Статьи в блоге'

    def __str__(self):
        return f'{self.article_head}\n{self.article_body}\n'
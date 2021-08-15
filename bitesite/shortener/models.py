from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Links(models.Model):
    original_url = models.URLField(max_length=255, verbose_name='Original url')
    shorten_url = models.CharField(max_length=25, blank=True, verbose_name='Short link', db_index=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Time create')
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Short URL for: {self.original_url} is {self.shorten_url}'

    def get_absolute_url(self):
        return reverse('redirect', kwargs={'slugs': self.shorten_url})

    class Meta:
        verbose_name = 'Links'
        verbose_name_plural = 'Links'
        ordering = ['-time_create', 'original_url']


class Feedback(models.Model):
    sender = models.EmailField(blank=True, verbose_name='Sender')
    message = models.TextField(verbose_name='Message')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
        ordering = ['-time_create', 'sender']

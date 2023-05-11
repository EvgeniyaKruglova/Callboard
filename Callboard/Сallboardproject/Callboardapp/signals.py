from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response


@receiver(post_save, sender=Response)
def response_created(instance, created, **kwargs):
    if not created:
        return
    email = instance.call.author.author_user.email

    subject = f'Новый отклик на объявление {instance.call.title}'

    text_content = (
        f'Автор: {instance.author.author_user.first_name} {instance.author.author_user.last_name}\n'
        f'Текст: {instance.text}\n\n'
        f'Ссылка на отклик: http://127.0.0.1{instance.get_absolute_url()}'
    )
    html_content = (
        f'Автор: {instance.author.author_user.first_name} {instance.author.author_user.last_name}<br>'
        f'Текст: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на отклик</a>'
    )
    msg = EmailMultiAlternatives(subject, text_content, None, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
#для форм авторизации
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#для нестандартной формы
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from Callboardapp.models import Author

# отправка писем
from django.core.mail import send_mail
# отправка писем c HTML
from django.core.mail import EmailMultiAlternatives
# отправка писем менеджерам и админам
from django.core.mail import mail_managers, mail_admins

#для стандартной формы
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

#для нестандартной формы
class CustomSignupForm(SignupForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        Author.objects.create(author_user=user)
        # отправка писем
        # тема
        subject = 'Добро пожаловать на нашу доску объявлений!'
        # текст
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/calls">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        # отправка писем менеджерам и админам
        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user
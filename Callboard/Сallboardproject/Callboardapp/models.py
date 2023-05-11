from django.db import models
# импорт юзера
from django.contrib.auth.admin import User
# импорт реверса для перехода на странцу объявления после заполнения формы
from django.urls import reverse
# для ckeditor
from ckeditor_uploader.fields import RichTextUploadingField

# модели приложения
class Author(models.Model):
   author_user = models.OneToOneField(User, on_delete=models.CASCADE)

   def __str__(self):
       return f'{self.author_user.first_name} {self.author_user.last_name} '

class Category(models.Model):
   name = models.CharField(max_length=64)

   def __str__(self):
       return f'{self.name}'

class Call(models.Model):
   author = models.ForeignKey(Author, on_delete=models.CASCADE)
   category = models.ManyToManyField(Category, related_name='CategoryCall')
   title = models.CharField(max_length=64)
   text = models.TextField()
   content = RichTextUploadingField(blank=True)

   def __str__(self):
       return f'{self.title}'

       # return f'{self.author.author_user.first_name} {self.author.author_user.last_name} ' \
       #        f'[{", ".join(category.name for category in self.category.all())}] ' \
       #        f'{self.title} ' \
       #        f'{self.text[:30]}'

   # функция реверс для перехода на определеную страницу после заполнения формы
   def get_absolute_url(self):
       return reverse('call_detail', args=[str(self.id)])

class Response(models.Model):
   author = models.ForeignKey(Author, on_delete=models.CASCADE)
   call = models.ForeignKey(Call, on_delete=models.CASCADE)
   text = models.TextField()
   STATUSES = [
       ('WAITING', 'Ожидает ответа'),
       ('ACCEPTED', 'Принят'),
   ]
   status = models.CharField(max_length=10, choices=STATUSES, default='WAITING')

   def __str__(self):
       return f'{self.author.author_user.first_name} {self.author.author_user.last_name} ' \
              f'{self.call.title}' \
              f'{self.text[:30]}'

   # функция реверс для перехода на определеную страницу после заполнения формы
   def get_absolute_url(self):
       return reverse('response_detail', args=[str(self.id)])


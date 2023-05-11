from django_filters import FilterSet
from .models import Call, Response

# Создаем фильтр
class CallFilter(FilterSet):
   class Meta:
       # Модель.
       model = Call
       # Поля
       fields = {
           'author': ['exact'],
           'category': ['exact'],
       }

class ResponseFilter(FilterSet):
   class Meta:
       # Модель.
       model = Response
       # Поля
       fields = {
           'author': ['exact'],
           'call': ['exact'],
       }
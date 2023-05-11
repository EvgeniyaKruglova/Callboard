# импорт форм
from django import forms
# импорт моделей
from .models import Call, Response
#для ckeditor
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# форма
class CallForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Контент')
    class Meta:
        # модель, на основе которой будет сделана форма
        model = Call
        # поля формы из модели
        fields = [
            #'author',
            'category',
            'title',
            'text',
            'content'
        ]
        # нестандартные (не из моделей) подписи к полям формы
        labels = {
                #'author': 'Автор',
                'category': 'Категория',
                'title': 'Заголовок',
                'text': 'Текст',
                'content': 'Контент'
                }
        # нестандартные окна ввода для полей
        widgets = {
            'category': forms.CheckboxSelectMultiple
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        # модель, на оснвое которой будет сделана форма
        model = Response
        # поля формы из модели
        fields = [
            #'author',
            #'call',
            'text',
        ]
        # нестандартные (не из моделей) подписи к полям формы
        labels = {
                #'author': 'Автор',
                #'call': 'Обявление',
                'text': 'Текст',
                }
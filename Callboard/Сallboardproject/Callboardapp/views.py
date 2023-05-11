from django.shortcuts import render

# импорт разных представлений
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# импорт моделей
from .models import Call, Response, Author
# импорт фильтров
from .filters import CallFilter, ResponseFilter
# импорт форм
from .forms import CallForm, ResponseForm
# импорт функция для возвращения на указанную страницу
from django.urls import reverse_lazy
# импорт перенарпавления на другой шаблон с вызванного представления
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
# импорт для ограничения прав
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

class CallsList(ListView):
    # Модель
    model = Call
    # Поле сортировки
    ordering = 'title'
    # Шаблон
    template_name = 'calls.html'
    # Объект для обращения в шаблоне
    context_object_name = 'calls'
    # Количество объектов на странице
    paginate_by = 3

    # Переопределяем функцию получения списка
    def get_queryset(self):
        # Получаем сет
        queryset = super().get_queryset()
        # Фильруем
        self.filterset = CallFilter(self.request.GET, queryset)
        # Возвращаем на страницу
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class CallDetail(DetailView):
    # Модель
    model = Call
    # Шаблон
    template_name = 'call.html'
    # Объект для обращения в шаблоне
    context_object_name = 'call'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CallCreate(PermissionRequiredMixin, CreateView):
    # Проверка прав
    permission_required = ('Callboardapp.add_call',)
    # Форма
    form_class = CallForm
    # Модель
    model = Call
    # Шаблон
    template_name = 'call_edit.html'

    # заполнение атрибута при создании объекта по умолчанию
    def form_valid(self, form):
        a = form.save(commit=False)
        a.author = Author.objects.get(author_user=self.request.user)
        a.save()
        return super().form_valid(form)

class CallUpdate(PermissionRequiredMixin, UpdateView):
    # Проверка прав
    permission_required = ('Callboardapp.change_call',)
    # Форма
    form_class = CallForm
    # Модель
    model = Call
    # Шаблон
    template_name = 'call_edit.html'

    def dispatch(self, request, *args, **kwargs):
        author = Call.objects.get(pk=self.kwargs.get('pk')).author.author_user
        if self.request.user == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Редактировать объявление может только его автор")

class CallDelete(PermissionRequiredMixin, DeleteView):
    # Проверка прав
    permission_required = ('Callboardapp.delete_call',)
    # Модель
    model = Call
    # Шаблон
    template_name = 'call_delete.html'
    # Перенаправление
    success_url = reverse_lazy('calls_list')

    def dispatch(self, request, *args, **kwargs):
        author = Call.objects.get(pk=self.kwargs.get('pk')).author.author_user
        if self.request.user == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Удалить объявление может только его автор")

class UserResponseList(ListView):
    # Модель
    model = Response
    # Поле сортировки
    ordering = 'call'
    # Шаблон
    template_name = 'user_responses.html'
    # Объект для обращения в шаблоне
    context_object_name = 'user_responses'
    # Количество объектов на странице
    paginate_by = 3

    # Переопределяем функцию получения списка
    def get_queryset(self):
        # Получаем сет отфильтрованных данных
        queryset = Response.objects.filter(call__author__author_user=self.request.user).order_by('id')
        # Фильруем
        self.filterset = ResponseFilter(self.request.GET, queryset)
        # Возвращаем на страницу
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class ResponseDetail(DetailView):
    # Модель
    model = Response
    # Шаблон
    template_name = 'response.html'
    # Объект для обращения в шаблоне
    context_object_name = 'response'

class ResponseCreate(PermissionRequiredMixin, CreateView):
    # Проверка прав
    permission_required = ('Callboardapp.add_response',)
    # Форма
    form_class = ResponseForm
    # Модель
    model = Response
    # Шаблон
    template_name = 'response_edit.html'

    # заполнение атрибута при создании объекта по умолчанию
    def form_valid(self, form):
        a = form.save(commit=False)
        a.author = Author.objects.get(author_user=self.request.user)
        a.call = Call.objects.get(id=self.kwargs.get('pk'))
        a.save()
        return super().form_valid(form)

# принятие отклика
@login_required
def response_accept(request, **kwargs):
    response = Response.objects.get(id=kwargs.get('pk'))
    response.status = 'ACCEPTED'
    response.save()
    return HttpResponseRedirect('/responses')


# удаление отклика
@login_required
def response_delete(request, **kwargs):
    response = Response.objects.get(id=kwargs.get('pk'))
    response.delete()
    return redirect('/responses')
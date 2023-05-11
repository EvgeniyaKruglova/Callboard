# импортируем пути и представления
from django.urls import path
from .views import CallsList, CallDetail, CallCreate, CallUpdate, CallDelete, ResponseDetail, ResponseCreate, UserResponseList, response_accept, response_delete

urlpatterns = [
   # подключаем представление объектов
   path('', CallsList.as_view(), name='calls_list'),
   # подключаем представление объекта через id
   path('<int:pk>', CallDetail.as_view(), name='call_detail'),
   path('create/', CallCreate.as_view(), name='call_create'),
   path('<int:pk>/update/', CallUpdate.as_view(), name='call_update'),
   path('<int:pk>/delete/', CallDelete.as_view(), name='call_delete'),
   path('responses', UserResponseList.as_view(), name='user_responses'),
   path('responses/<int:pk>', ResponseDetail.as_view(), name='response_detail'),
   path('responses/<int:pk>/create/', ResponseCreate.as_view(), name='response_create'),
   path('responses/<int:pk>/accept', response_accept, name='response_accept'),
   path('responses/<int:pk>/delete', response_delete, name='response_delete'),
]
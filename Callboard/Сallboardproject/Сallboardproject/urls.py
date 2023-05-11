"""
URL configuration for Сallboardproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# вставляем include для url приложения
from django.urls import path, include

# для ckeditor
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
    path('admin/', admin.site.urls),
    # для allauth
    path("accounts/", include("allauth.urls")),
    # вставляем url приложения
    # для выхода в адреса
    # path('calls/', include('Callboardapp.urls')),
    # для выхода на главную
    path('', include('Callboardapp.urls')),
    # для ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # для авторизации
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include("accounts.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

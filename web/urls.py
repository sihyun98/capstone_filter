"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
import picture.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', picture.views.home, name = "home"),
    path('recommend/', picture.views.detection_crawler, name = "recommend"),
    path('search/', picture.views.search_crawler, name="search"),
    #path('recommendation/', picture.views.recommendation, name="recommendation"),
    #path('result/', picture.views.result, name="result"),
    #path('create', picture.views.create, name='create'),
    # path('new/', picture.views.new, name='new'),
    # path('upload/', picture.views.upload, name='upload'),
    #path('image/', picture.views.image, name="image"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
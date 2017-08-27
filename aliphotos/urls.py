"""aliphotos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from photos import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.best, {'interval': 'day'}),
    url(r'^week/$', views.best, {'interval': 'week'}),
    url(r'^month/$', views.best, {'interval': 'month'}),
    url(r'^all/$', views.best, {'interval': 'all'}),
    url(r'^photo/(?P<photo_id>\d+)/$', views.detail),
    url(r'^photos/send/$', views.send_photos),
    url(r'^photos/like/$', views.like, name='like'),
    url(r'^photos/flag/$', views.flag, name='flag'),
    url(r'^items/$', views.items),
    url(r'^item/(?P<item_id>\w+)/$', views.item_detail),
    url(r'^categories/$', views.categories),
    url(r'^category/(?P<category_id>\w+)/$', views.category_detail),
    url(r'^new/$', views.new, name='new'),
    url(r'^add/$', views.add_photos, name='add'),
]

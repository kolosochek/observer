# -*- coding: utf-8 -*-
"""observer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from views import tickets_view, logout
from django.contrib.staticfiles import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import settings

urlpatterns = [
    url(r'^$', tickets_view),
    url(r'^logout/', logout),
    url(r'^tickets/(?P<url>[a-zA-Z-_0-9&=]*)/(?P<mode>[a-z]*)/(?P<content_type>\w+)$', tickets_view),
    url(r'^tickets/', admin.site.urls),
    # Define static
    url(r'^static/(?P<path>.*)$', views.serve),
]
urlpatterns += staticfiles_urlpatterns()
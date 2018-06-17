"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

from django.conf.urls import url,include
from django.contrib import admin

from blog.feeds import AllPostsRssFeed

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'',include('blog.urls')),
    url(r'',include('comments.urls')),
    
    url(r'^all/rss/$',AllPostsRssFeed(),name='rss'),
    #RSS
    
    #url(r'^users/',include('users.urls')),
    #用户认证系统
]
#前面建立了一个 urls.py 文件，并且绑定了 URL 和视图函数 index，但是 Django 并不知道。

#把 blog 应用下的 urls.py 文件包含到 blogproject\urls.py 里去
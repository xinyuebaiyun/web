from django.conf.urls import url 
from . import views

app_name='comments'
#给这个评论的 URL 模式规定命名空间
urlpatterns=[
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$',views.post_comment,name='post_comment'),
]



#最后还要在项目的 blogprokect\ 目录的 urls.py 里包含 comments\urls.py 这个文件
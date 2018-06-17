from django.conf.urls import url

from . import views



app_name='blog'
urlpatterns=[
    url(r'^$',views.IndexView.as_view(),name='index'), 
    #as_view方法把类视图转换为视图函数
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^about$', views.about, name='about'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    url(r'^archives$',views.all_archives,name='all_archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^category$',views.all_category,name='all_category'),

    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^search/$',views.search,name='search'),


]
#url的第一个参数是网址域名，Django用正则表达式来匹配用户访问的网站
#第一个url()对应网站首页，第二个url()对应文章详情页，第三四个对应侧边栏归档分类点击详情页


#当用户访问某个网址时，Django 就去会到此文件里查找，
#如果找到这个网址，就会调用和它绑定处理函数（叫做视图函数），
#视图函数惯例在view.py文件里
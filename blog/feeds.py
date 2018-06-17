from django.contrib.syndication.views import Feed
from .models import Post

class AllPostsRssFeed(Feed):
    title=" 郭云飞个人博客 "
    #聚合阅读器上的标题
    link="/"
    #通过聚合阅读器跳转到网站的地址
    description="来自<www.guoyunfei.online>"
    
    def items(self):
        return Post.objects.all()
    #内容条目
    def item_title(self,item):
        return '[%s] %s' % (item.category,item.title)
    #内容条目的标题
    def item_description(self,item):
        return item.body
    #描述

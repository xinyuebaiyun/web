from django.db import models
#from django.utils.six import python_2_unicode_compatible用于兼容python2

class Comment(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=255)
    url=models.URLField(blank=True)  
    #blank=True规定可以没有个人网站url
    text=models.TextField()  #用户发布的评论内容
    created_time=models.DateTimeField(auto_now_add=True)
    #auto_now_add=True自动指定当前时间为created_time
    
    post=models.ForeignKey('blog.Post')
    #此评论一对一的对应一个Post（文章）
    
    def _str_(self):
        return self.text[:20]





# Create your models here.

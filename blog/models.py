from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

import markdown
from django.utils.html import strip_tags

@python_2_unicode_compatible
class Category(models.Model):
    name=models.CharField(max_length=100)#Charfield是字符型
    def  __str__(self):
        return self.name
class Tag(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Post(models.Model):
    title=models.CharField(max_length=70)
    body=models.TextField()
    created_time=models.DateTimeField()
    modified_time=models.DateTimeField()
    excerpt=models.CharField(max_length=200,blank=True)#摘要
    category=models.ForeignKey(Category)
    tags=models.ManyToManyField(Tag,blank=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL)
    views=models.PositiveIntegerField(default=0)
    #views字段用于存储阅读量
    #PositiveIntegerField类型的值只允许为正整数或0，初始为0    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
    class Meta:
        ordering=['-created_time']
        #内部类Meta通过指定一些属性来规定这个类该有的一些特性
        #内部类Meta的属性ordering指定Post的排序方式
        #['-created_time']指定依据created_time属性排序
        #结果就是Post按照发布时间晚的在前，早的在后的顺序排列
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
        # update_fields 参数作用是让Django 只更新数据库中 views 字段的值，以提高效率
        #save views字段的值到数据库
    def save(self,*args,**kwargs):
        if not self.excerpt:
        #当摘要没有填写时
            md=markdown.Markdown(extensions=[
               'markdown.extensions.extra',
               'markdown.extensions.codehilite',
            ])
            #实例化一个markdown类，用于渲染body文本
            
            self.excerpt=strip_tags(md.convert(self.body))[:54]
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
        super(Post,self).save(*args,**kwargs)
        #保存数据
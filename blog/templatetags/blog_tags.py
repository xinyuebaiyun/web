#   blogproject\blog\templatetags\blog_tags.py
from ..models import Post,Category,Tag

from django import template

from django.db.models.aggregates import Count

register=template.Library()
#导入 template 模块，实例化了一个 template.Library 类

#‘最新文章’模板标签
@register.simple_tag
def get_recent_posts(num=2):
    return Post.objects.all().order_by('-created_time')[:num]
#按照创建时间顺序获取数据库中前num=5篇Post.
#Django 在模板中不知道该如何使用一个纯 Python 函数
#将函数 get_recent_posts 装饰为 register.simple_tag
#这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了。

#‘归档’模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')
#dates 方法会返回一个‘元素为每一篇文章（Post）的创建时间’的列表
#且是 Python 的 date 对象，精确到月份，降序排列。
#三个参数分别表示：创建时间、精度、降序排列

#‘分类’模板标签
@register.simple_tag
def get_categories():
    #return  Category.objects.all 
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
#从数据库中获取所有分类（Category）

#Category.objects.annotate 方法和 Category.objects.all 有点类似，
#它会返回数据库中全部 Category 的记录，但同时它还会做一些额外的事情
#在这里额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。
#Count 方法接收一个和 Categoty 相关联的模型参数名,
#这里是 Post，通过category=models.ForeignKey(Category)关联的
#然后便会统计 Category 记录的集合中每条记录下与之关联的 Post 记录的行数,
#即某个分类的文章数，最后把文章数保存到num_posts属性中

#此外，还用filter过滤掉了文章数小于1的分类
#gt就是greate than,表示大于

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
#get_tags模板标签

from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm 

def post_comment(request,post_pk):
    post=get_object_or_404(Post,pk=post_pk)
    #获取被评论的Post
    if request.method=='POST':  
    #判断用户发送的HTTP请求是否为POST类型的（HTTP请求有GET、POST两种）
        form=CommentForm(request.POST)
        #request.POST表示用户发布的数据，是个类字典对象
        #以它为参数，form成为了CommetForm类的一个实例，即一个表单
        if form.is_valid():
        #判断form表格的数据形式是否合格
            comment=form.save(commit=False)
            #save方法把表单数据保存到数据库
            #commit=False参数作用是用表单的数据生成 Comment 模型类的实例
            
            comment.post=post #把评论和被评论的文章关联起来
                              #？？？？？？？
            comment.save()
            #save方法保存到数据库
            return redirect(post)
            #重定向到被评论 Post 的详情页，
            #当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            #然后重定向到 get_absolute_url 方法返回的 URL。
        else:#表格数据形式不合格
             #重新渲染详情页，并且渲染表单的错误。
            comment_list=post.comment_set.all()
            #定义一个list为该文章的全部评论
            
            #comment_count=post_comment_set.count()
            context={'post':post,
                    'form':form,
                    'comment_list':comment_list
                    }
            #把三个模板变量'post','form','comment_list'传给detail.html
            
            return render(request,'blog/detail.html',context=context)
    return redirect(post)
    #HTTP请求不是POST类型，
    #说明用户没有提交数据 ，重定向到该文章详情页              #
                    #
                    #
                    #
                    #
                    #
                    
                    #
                    #
                    
                    #
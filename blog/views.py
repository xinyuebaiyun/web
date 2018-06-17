from django.shortcuts import render
from django.http import HttpResponse

from .models import Post,Category,Tag
from django.shortcuts import render,get_object_or_404

import markdown

from comments.forms  import CommentForm#评论

from django.views.generic import ListView,DetailView

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from django.db.models import Q

class IndexView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'
    #将 index 视图函数改写为类视图
    #继承于ListView类视图，ListView 是从数据库中获取某个模型列表数据的
    #三个属性model、template_name、context_object指定此视图函数要做的事
    #将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
    #template_name指定为blog/index.html。指定这个视图渲染的模板。
    #context_object_name指定获取的模型列表数据保存为的变量名。这个变量传递给模板。
    paginate_by=5
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    
    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

class CategoryView(IndexView):
    #指定的属性值和IndexView相同，直接继承
    def get_queryset(self):
        cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)
    #get_queryset 方法默认获取指定模型的全部列表数据。
    #为了获取指定分类下的文章列表数据，需覆写该方法改变它的默认行为。
    # self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值
    #对get_queryset 方法获得的全部文章列表调用 filter 方法来筛选该分类下的全部文章并返回
    
class ArchivesView(IndexView):
    def get_queryset(self):
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(created_time__year=year,
                                                              created_time__month=month
                                                              ).order_by('-created_time')
    
class PostDetailView(DetailView): #继承于DetailView类
        model=Post
        template_name='blog/detail.html'
        context_object_name='post'
        
        def get(self,request,*arg,**kwargs):
            response=super(PostDetailView,self).get(request,*arg,**kwargs)
            # get 方法返回的是一个 HttpResponse 实例
            #只有当 get 方法被调用后，才有 self.object 属性
            #其值为 Post 模型实例，即被访问的文章 post
            self.object.increase_views()
            #阅读量+1
            return response
            #视图必须返回一个 HttpResponse 对象
        #get()函数作用是当文章被访问时，调用increase_views()，阅读量+1
        
        def get_object(self,queryset=None):
            post=super(PostDetailView,self).get_object(queryset=None)
            md= markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                #代码高亮
                TocExtension(slugify=slugify),
                #自动生成目录
            ])
        #实例化了一个 markdown.Markdown 类 md
            post.body=md.convert(post.body)
            #用实例的convert方法把Markdown 文本渲染成 HTML 文本
            post.toc=md.toc
            #md.toc的值为内容的目录，传给post.toc
            return post
        #get_object()函数作用是把Post的body渲染成markdown形式
        
        def get_context_data(self,**kwargs):
            context=super(PostDetailView,self).get_context_data(**kwargs)
            form=CommentForm()
            comment_list=self.object.comment_set.all()
            context.update({
                'form':form,
                'comment_list':comment_list
            })
            return context
            #返回的值是一个字典，这个字典就是模板变量字典，最终会被传递给模板。
        #get_context_data()作用是把文章对应的评论表单、评论列表传递给模板
        
            
def all_archives(request):
    date_list=Post.objects.dates('created_time', 'month', order='DESC')
    return render(request,'blog/archives.html',context={'date_list' : date_list})
    
def all_category(request):
    category_list=Category.objects.all()
    return render(request,'blog/category.html',context={'category_list' : category_list})
    
#上面两个函数all-archives、all_category分别是右上角导航栏“归档”、“分类”按钮的视图函数

class TagView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'
    
    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)
    
    
def search(request):
    q=request.GET.get('q')
    #表单中搜索框 input 的 name 属性的值是 q
    #用get方法从request.GET中获取用户提交的关键词q
    error_msg=''
    #下面判断q是否为空，q是空的话返回模板一个错误提示信息
    #q有值的话，用filter过滤出全部title或者body含有q的Post并赋值成一个list
    #然后返回模板错误提示信息为空，list为过滤出的Post
    if not q:
        error_msg="请输入关键词"
        return render(request,'blog/index.html',{'error_msg':error_msg})
    post_list=Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request,'blog/index.html',{'error_msg': error_msg,
                                            'post_list': post_list})
                                            
def about(request):
    
    return render(request,'blog/about.html',context={})
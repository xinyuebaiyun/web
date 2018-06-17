from django.contrib import admin
from .models import Post,Category,Tag

class PostAdmin(admin.ModelAdmin):
    list_display=['title','created_time','modified_time','category','author']
#在 admin post 列表页面只看到了文章标题，要显示更详细信息，需要定制 Admin 
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)


# Register your models here.
#在Admin后台注册模型，Post、Category、Tag
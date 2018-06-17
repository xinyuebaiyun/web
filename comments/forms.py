#表单
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):#表单类必须继承自forms.Form类或者forms.ModelForm类
    class Meta:        #表单的内部类Meta
        model=Comment   #内部类 Meta 指定Comment，表明这个表单对应的数据库模型是Comment类
        fields=['name','email','url','text']#指定表单显示的字段
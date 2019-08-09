from django.contrib import admin
from .models import Comment
from Blog_sys.base_admin import BaseOwnerAdmin
from xadmin.layout import Row,Fieldset,Container
import xadmin
# Register your models here.
@xadmin.sites.register(Comment)
class CommentAdmin ():
    list_display = ('target','content','nickname','status','created_time')
    form_layout = (
        Fieldset(
            '评论内容',
            Row("nickname","content"),
            'status',
            'created_time'
        )
    )
    # form_layout = (
    #     Container(
    #         '评论内容',
    #         Row("nickname","content"),
    #         'status',
    #         'created_time'
    #     )
    # )
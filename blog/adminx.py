from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from Blog_sys.base_admin import BaseOwnerAdmin
from Blog_sys.custom_site import custom_site
from xadmin.layout import Row,Fieldset
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
import xadmin
# Register your models here.


# 内置编辑文章
class PostInline(admin.TabularInline):
    fields = ('title','desc')
    extra = 1
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin (BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','owner','post_count')
    fields = ('name','status','is_nav')
    inlines = [PostInline,]

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@xadmin.sites.register(Tag)
class TagAdmin (BaseOwnerAdmin):
    list_display = ('name','status','created_time','owner')
    fields = ('name','status')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)


""" 自定义过滤器只展示当前用户分类 """
class CategoryOwnerFilter(RelatedFieldListFilter):


    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id','name')
manager.register(CategoryOwnerFilter,take_priority=True)

@xadmin.sites.register(Post)
class PostAdmin (BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title','category','status','created_time','owner','operator')#'operator'
    list_display_links = []
    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title','category__name'] #可以根据标题和分类来搜索
    actions_on_top = True
    actions_on_bottom = False
    save_on_top = True
    exclude = ('owner',)
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )
    list_filter = ['category']
    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'
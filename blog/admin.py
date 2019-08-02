from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from Blog_sys.base_admin import BaseOwnerAdmin
from Blog_sys.custom_site import custom_site
# Register your models here.


# 内置编辑文章
class PostInline(admin.TabularInline):
    fields = ('title','desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin (BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','owner','post_count')
    fields = ('name','status','is_nav')
    inlines = [PostInline,]

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag,site=custom_site)
class TagAdmin (BaseOwnerAdmin):
    list_display = ('name','status','created_time','owner')
    fields = ('name','status')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)


""" 自定义过滤器只展示当前用户分类 """
class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        Category_id = self.value()
        if Category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
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
    fieldsets = (
        ('基础信息',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'content'
            )
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('tag',),
        })
    )
    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'content',
    #     'status',
    #     'tag',
    # )
    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('custom_site:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'
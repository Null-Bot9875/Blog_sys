from django.contrib import admin

class BaseOwnerAdmin(object):
    """
    1.用来自动补充文章，分类，标签，侧边栏，友链这些model的owner字段
    2.用来针对queryset 过滤当前用户的数据
    """
    exclude = ('owner', )


    # 让用户只看到自己写的文章
    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner = request.user)
        # qs = super(BaseOwnerAdmin,self).get_queryset(request)
        # return qs.filter(owner = request.user)

    # 保存时自动添加作者属性
    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()
        # obj.owner = request.user
        # return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)
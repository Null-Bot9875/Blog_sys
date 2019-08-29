from dal import autocomplete

from blog.models import Category,Tag

class CategoeyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        #输入是self.q 输出为 queryset()
        if not self.request.user.is_authenticated():
            #如果是未登录用户，直接返回空的querset
            return Category.objects.none()
        #获取该用户创建的所有分类或者标签
        qs = Category.objects.filter(owner=self.request.user)
# """
#     .. py:attribute:: q
#       q是url上参数传来的值
#      Query string as typed by the user in the autocomplete field.
# """
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class TagAutocomplete (autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()
        qs = Tag.objects.filter(owner=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
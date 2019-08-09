from django.contrib import admin
from .models import Link,SideBar
from Blog_sys.base_admin import BaseOwnerAdmin
from xadmin.layout import Row,Fieldset
import xadmin
# Register your models here.
@xadmin.sites.register(Link)
class LinkAdmin (BaseOwnerAdmin):
    list_display = (
        'title',
        'href',
        'status',
        'weight',
        'created_time'
    )
    Fieldset(
        'title',
        'href',
        'status',
        'weight',
        'created_time'
    )
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin,self).save_model(request,obj,form,change)


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')
    Fieldset(
        'title', 'display_type', 'content', 'created_time'
    )
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)
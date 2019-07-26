from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = 'Blog_sys'
    site_title = '博客管理后台'
    index_title = '首页'

custom_site = CustomSite(name='custom_site')
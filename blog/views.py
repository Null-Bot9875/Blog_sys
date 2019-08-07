from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect
from django.views.generic import DetailView,ListView,TemplateView
from .models import Post,Tag,Category
from Comment.forms import CommentForm
from Comment.models import Comment
from config.models import SideBar,Link
# Create your views here.

class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       # urls = SideBar.get_all().filter() 侧边栏中没有文章链接 需要传过去
        context.update({
            'sidebars':SideBar.get_all(),
        })
        context.update(Category.get_navs())
        #print("\n\nCommViewMixin print : " +"kwargs = " , str(kwargs) + "\n\ncontext = ",str(context) + "\n\nself = ",str(self))
        return context

class IndexView(CommonViewMixin,ListView):
    queryset = Post.latest_posts()
    paginate_by = 3
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class SearchView (IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword','')
        })
        print("SearchView 的上下文 : ",context)
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            print("搜索筛选的queryset print: ", keyword,"\n queryset",queryset)
            return queryset
        print("搜索筛选的queryset print: ", keyword, "\n queryset", queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword)))
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

class PostListView(CommonViewMixin,ListView):
    queryset = Post.latest_posts()
    paginate_by = 3 # 每页的文章数量
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class LinklistView(ListView,CommonViewMixin):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'

class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'categoriy':category,
        })
        #print("\n\nCategoryView print : " +"kwargs = ", str(kwargs) + "\n\ncontext = ",str(context) + "\n\nself = ",str(self))
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
           'tag': tag,
        })
        #print("\n\nTagView print : " +"\n\nkwargs = ", str(kwargs) + "\n\n  context = ",str(context) + "self = ",str(self))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form':CommentForm,
    #         'comment_list':Comment.get_by_target(self.request.path),
    #     })
    #     #print("PostDetailView get_context_data",context)
    #     return context


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)
class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'
    def post(self,request,*args,**kwargs):
        comment_form  = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            print("CommentView POST ", instance)
            print("CommentView target (target path) ", target)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
        context = {
            'succeed':succeed,
            'form':comment_form,
            'target':target,
        }
        print("CommentView Context ", context)
        return self.render_to_response(context)
def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post':post,
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html',context=context)

def post_list(request,category_id=None,tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list,tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list,category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'categories': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars':SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request,'blog/list.html',context=context)
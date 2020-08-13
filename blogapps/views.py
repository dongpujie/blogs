import re
import markdown
from django.contrib.auth.models import User
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from pure_pagination import PaginationMixin

from .models import Post, Category, Tag


# def index(request):
#     # 首页
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blogapps/index.html', context={'post_list': post_list})

# def detail(request, pk):
#     # 详情页
#     post = get_object_or_404(Post, pk=pk)
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         # 优化锚点
#         TocExtension(slugify=slugify),
#         # 'markdown.extensions.toc',
#     ])
#     post.body = md.convert(post.body)
#     # 判断有没有文章目录
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = md.toc if m.group(1) else ''
#
#     # 阅读量 +1
#     post.increase_views()
#
#     return render(request, 'blogapps/detail.html', context={'post': post})


# class DetailView(generic.DetailView):
#     # 详情页
#     model = Post
#     template_name = "blogapps/detail.html"
#     context_object_name = 'post'


# def archive(request, year, month):
#     # 归档页面
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     ).order_by('-created_time')
#     return render(request, 'blogapps/index.html', context={'post_list': post_list})
#
#
# def category(request, pk):
#     # 分类页面
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blogapps/index.html', context={'post_list': post_list})
#
#
# def tag(request, pk):
#     # 标签页面
#     t = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=t).order_by('-created_time')
#     return render(request, 'blogapps/index.html', context={'post_list': post_list})
#
#
# def zuozhe(request, pk):
#     # 作者页面
#     z = get_object_or_404(User, pk=pk)
#     post_list = Post.objects.filter(author=z).order_by("-created_time")
#     return render(request, 'blogapps/index.html', context={'post_list': post_list})


class IndexView(PaginationMixin, generic.ListView):
    # 首页
    model = Post
    template_name = 'blogapps/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-created_time')


class ArchiveView(IndexView):
    # 归档页面
    def get_queryset(self):
        # 从 URL 捕获的路径参数值保存在实例的 kwargs 属性（是一个字典）里，非路径参数值保存在实例的 args 属性（是一个列表）里
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


class CategoryView(IndexView):
    # 分类页面
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    # 标签页面
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


class ZuozheView(IndexView):
    # 作者页面
    def get_queryset(self):
        zuozhe = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return super(ZuozheView, self).get_queryset().filter(author=zuozhe)


class ReadView(IndexView):
    # 阅读量页面
    def get_queryset(self):
        return super(ReadView, self).get_queryset().order_by('-views')


class PostDetailView(generic.DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blogapps/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    # def get_object(self, queryset=None):
    #     # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
    #     post = super().get_object(queryset=None)
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         # 记得在顶部引入 TocExtension 和 slugify
    #         TocExtension(slugify=slugify),
    #     ])
    #     post.body = md.convert(post.body)
    #
    #     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     post.toc = m.group(1) if m is not None else ''
    #
    #     return post

import re
import markdown

from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Category, Tag


# def index(request):
#     # 首页
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blogapps/index.html', context={'post_list': post_list})

def detail(request, pk):
    # 详情页
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 优化锚点
        TocExtension(slugify=slugify),
        # 'markdown.extensions.toc',
    ])
    post.body = md.convert(post.body)
    # 判断有没有文章目录
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = md.toc if m.group(1) else ''

    return render(request, 'blogapps/detail.html', context={'post': post})


class IndexView(generic.ListView):
    # 首页
    template_name = 'blogapps/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_time')


# class DetailView(generic.DetailView):
#     # 详情页
#     model = Post
#     template_name = "blogapps/detail.html"
#     context_object_name = 'post'


def archive(request, year, month):
    # 归档页面
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blogapps/index.html', context={'post_list': post_list})


def category(request, pk):
    # 分类页面
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blogapps/index.html', context={'post_list': post_list})


def tag(request, pk):
    # 标签页面
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blogapps/index.html', context={'post_list': post_list})

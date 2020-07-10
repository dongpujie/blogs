from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views import generic


# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blogapps/index.html', context={'post_list': post_list})

# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/detail.html', context={'post': post})


class IndexView(generic.ListView):
    template_name = 'blogapps/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_time')


class DetailView(generic.DetailView):
    model = Post
    template_name = "blogapps/detail.html"
    context_object_name = 'post'

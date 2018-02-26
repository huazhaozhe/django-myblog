from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.decorators import method_decorator
from datetime import datetime
from .models import Category, Tag, Post
from .forms import PostForm
from comment.forms import CommentForm
from django.db.models import Q
from accounts.models import User
import json, collections

from_email = settings.EMAIL_HOST_USER
to_email = [settings.ADMINS[0][1]]

def check_superuser(user):
    return user.is_superuser

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})

class PostIndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(visible=True, status=1)

    def get_context_data(self, **kwargs):
        context = super(PostIndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.paginate_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def paginate_data(self, paginator, page, is_paginated, num=3):
        if not is_paginated:
            return {}
        page_number = page.number
        num_pages = paginator.num_pages
        if page_number < 1 or page_number > num_pages:
            page_number = 1
        left_more = True
        right_more = True
        left_num = page_number - num
        left_more_num = left_num - 1
        right_num = page_number + num
        right_more_num = right_num + 1
        if left_num <= 1:
            left_num = 1
            left_more = False
            left_more_num = left_num
        if right_num >= num_pages:
            right_num = num_pages
            right_more = False
            right_more_num = right_num
        page_list = list(range(left_num, right_num+1))
        data = {
                'page_number': page_number,
                'num_pages': num_pages,
                'left_more': left_more,
                'right_more': right_more,
                'left_more_num': left_more_num,
                'right_more_num': right_more_num,
                'page_list': page_list
                }
        return data


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
            'post': post,
            'form': form,
            'comment_list': comment_list
            }
    return render(request, 'blog/detail.html', context=context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        if self.request.user.is_superuser:
            return response
        elif self.object.visible and self.object.status == 1:
            self.object.increase_views()
            return response
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.get_comments()
        context.update({
            'form': form,
            'comment_list': comment_list
            })
        return context

@login_required(login_url='/account/login')
@permission_required('blog.add_post', 'blog.change_post', 'blog.delete_post')
def add_or_edit(request, pk=0):

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if pk != 0 and pk != '0':
                post = get_object_or_404(Post, pk=pk)
                form = PostForm(request.POST, instance=post)
            post = form.save()
            json_data = json.loads(post.json_data)
            new_category = json_data['new_category']
            new_tags = json_data['new_tags']
            modified_date = json_data['datetime']['date']
            modified_time = json_data['datetime']['time']
            if modified_date and modified_time:
                modified_time = datetime.strptime(modified_date+' '+modified_time, '%Y/%m/%d %I:%M%p')
                post.modified_time = modified_time
            else:
                post.modified_time = timezone.now()
            if new_category:
                category_new = Category.objects.get_or_create(name=new_category)
                post.category = category_new[0]

            if new_tags:
                for tag in new_tags:
                    new_tag = Tag.objects.get_or_create(name=tag)
                    post.tags.add(new_tag[0])
            post.save()
            return redirect(post)
        return render(request, 'blog/post_edit.html', context = {'pk': pk, 'form': form})
    if pk != 0 and pk != '0':
        pk = pk
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
    else:
        pk = 0
        form = PostForm()
    context = {'pk': pk, 'form': form}

    return render(request, 'blog/post_edit.html', context=context)

class PostAddOrEditView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    context_object_name = 'form'

    @method_decorator(user_passes_test(check_superuser))
    def dispatch(self, *args, **kwargs):
        return super(PostAddOrEditView, self).dispatch(*args, **kwargs)

    #重写get_object是因为使用UpdateView新建post时没有pk会出错,参照CreateView返回None
    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk', '')
        if pk:
            obj = get_object_or_404(self.model, pk=pk)
        else:
            obj = None
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostAddOrEditView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', '')
        context.update({'pk': pk})
        return context

    #直接新建category和tags并更新
    def new_category_or_tags(self):
        json_data = json.loads(self.object.json_data)
        new_category = json_data['new_category']
        new_tags = json_data['new_tags']
        modified_date = json_data['datetime']['date']
        modified_time = json_data['datetime']['time']
        if modified_date and modified_time:
            modified_time = datetime.strptime(modified_date+' '+modified_time, '%Y/%m/%d %I:%M%p')
            self.object.modified_time = modified_time
        else:
            self.object.modified_time = timezone.now()
        if new_category:
            category_new = Category.objects.get_or_create(name=new_category)
            self.object.category = category_new[0]
        if new_tags:
            for tag in new_tags:
                new_tag = Tag.objects.get_or_create(name=tag)
                self.object.tags.add(new_tag[0])
        self.object.save()

    def form_valid(self, form):
        if self.object:
            form.save()
        else:
            #新建post
            self.object = form.save()
        self.new_category_or_tags()
        return self.get_success_url()

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return redirect(self.object)


#@login_required(login_url='/account/login')
#@permission_required('blog.add_post', 'blog.change_post', 'blog.delete_post')
@user_passes_test(check_superuser)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    try:
        send_mail('django-blog-delete', post.title, from_email, to_email)
    except:
        pass
    return redirect(reverse('blog:index'))

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

class ArchivesView(PostIndexView):

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(PostIndexView):

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

class TagView(PostIndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)



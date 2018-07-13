from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse


# Create your views here.

from .models import Comment
from .forms import CommentForm

from blog.models import Post


@login_required(login_url='/account/login/')
@permission_required('comment.add_comment')
def post_comment(request, post_pk, parent_comment_pk=0):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            if parent_comment_pk != '0' and parent_comment_pk != 0:
                parent_comment = get_object_or_404(Comment, pk=parent_comment_pk)
            else:
                parent_comment = None
            comment = form.save(False)
            comment.user = request.user
            comment.post = post
            comment.parent_comment = parent_comment
            comment.save()

            comment_list = post.get_comments()
            form = CommentForm()
            context = {
                    'post': post,
                    'form': form,
                    'comment_list': comment_list
                    }

            return render(request, '_comments.html', context=context)
        return HttpResponse('ajax_error')
    raise SuspiciousOperation


@login_required(login_url='/account/login/')
def comment_delete(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        post = comment.post
        if request.user.is_superuser:
            comment.delete()
            form = CommentForm()
            comment_list = post.get_comments()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            # return redirect(post)
            return render(request, '_comments.html', context=context)
    raise SuspiciousOperation


@login_required(login_url='/account/login/')
def comment_enable(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        post = comment.post
        if request.user.is_superuser:
            comment.enable = not comment.enable
            comment.save()
            form = CommentForm()
            comment_list = post.get_comments()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            # return redirect(comment.post)
            return render(request, '_comments.html', context=context)
    raise SuspiciousOperation
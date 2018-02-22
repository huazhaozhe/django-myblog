from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

from .models import Comment
from .forms import CommentForm

from blog.models import Post


@login_required(login_url='/account/login/')
@permission_required('comment.add_comment')
def post_comment(request, post_pk, parent_comment_pk=0):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=post_pk)
            if parent_comment_pk != '0' and parent_comment_pk != 0:
                parent_comment = get_object_or_404(Comment, pk=parent_comment_pk)
            else:
                parent_comment = None
            comment = form.save(False)
            comment.user = request.user
            comment.post = post
            comment.parent_comment = parent_comment
            comment.save()
            return redirect(post)
        else:
            comment_list = post.get_comments()
            context = {
                    'post': post,
                    'form': form,
                    'comment_list': comment_list
                    }
        return render(request, 'blog/detail.html', context=context)
    return redirect(post)

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    comment.delete()
    return redirect(post)

def comment_enable(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.enable = not comment.enable
    comment.save()
    return redirect(comment.post)

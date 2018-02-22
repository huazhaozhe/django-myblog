from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post
from note.models import Note
from .models import Home

def home(request):
    return render(request, 'home/home.html')

def about(request):
    home = get_object_or_404(Home, pk=1)
    return render(request, 'home/about.html', context={'about': home.about})

def not_found(request):
    return render(request, 'home/error.html', {'message': '你访问的地方已经回家过年了', 'status_code': 404}, status=404)

def server_error(request):
    return render(request, 'home/error.html', {'message': '程序猿的bug能叫bug吗?', 'status_code': 500}, status=500)

def permission_denied(request):
    return render(request, 'home/error.html', {'message': '啊, 这个不可以', 'status_code': 403}, status=403)

def bad_request(request):
    return render(request, 'home/error.html', {'message': '呃,你有点无聊', 'status_code': 400}, status=400)

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django import forms
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from .models import Note
from accounts.models import User
from .forms import NoteForm
import os, json

from_email = settings.EMAIL_HOST_USER
to_email = [settings.ADMINS[0][1]]

class NoteIndexView(ListView):
    model = Note
    template_name = 'note/index.html'
    context_object_name = 'note_list'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(NoteIndexView, self).get_context_data(**kwargs)
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


@login_required(login_url='/account/login')
#@permission_required('note.add_note', 'note.change_note', 'note.delete_note')
def add_or_edit(request, pk=0):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(False)
            if note.image_url or note.title:
                if pk != 0 and pk != '0':
                    note = get_object_or_404(Note, pk=pk)
                    if request.user == note.author or request.user.is_superuser:
                        form = NoteForm(request.POST, instance=note)
                        note = form.save()
                    else:
                        raise PermissionDenied
                else:
                    note.author = request.user
                    note.save()
                return redirect(reverse('note:index'))
        return render(request, 'note/note_edit.html', context = {'pk': pk, 'form': form})
    if pk != 0 and pk != '0':
        pk = pk
        note = get_object_or_404(Note, pk=pk)
        if request.user == note.author or request.user.is_superuser:
            form = NoteForm(instance=note)
        else:
            raise PermissionDenied
    else:
        pk = 0
        form = NoteForm()
    context = {'pk': pk, 'form': form}
    return render(request, 'note/note_edit.html', context=context)

def note_like(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    note.increase_likes()
    return redirect(reverse('note:index'))

@login_required(login_url='account/login')
def note_delete(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    next = request.GET.get('next', reverse('note:index'))
    if request.user == note.author or request.user.is_superuser:
        note.delete()
        return redirect(next)
    else:
        raise PermissionDenied

def note_visible(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    note.visible = not note.visible
    note.save()
    return redirect('/note/')


class NoteAddOrEditView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note/note_edit.html'

    @method_decorator(login_required(login_url='account/login'))
    def dispatch(self, *args, **kwargs):
        return super(NoteAddOrEditView, self).dispatch(*args, **kwargs)

    #重写get_object是因为使用UpdateView新建note时没有pk会出错,参照CreateView返回None
    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk', '')
        if pk:
            obj = get_object_or_404(self.model, pk=pk)
        else:
            obj = None
        return obj

    def get_context_data(self, **kwargs):
        context = super(NoteAddOrEditView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', '')
        context.update({'pk': pk})
        return context

    def form_valid(self, form):
        if self.object:
            if self.object.author == self.request.user or self.request.user.is_superuser:
                form.save()
            else:
                raise PermissionDenied
        else:
            #新建note
            note = form.save(False)
            note.author = self.request.user
            note.save()
            self.object = note
            new_note_email_message = '''
                nickname: %s,
                email: %s,
                title: %s,
                image_url: %s
                ''' % (note.author.nickname, note.author.email, note.title, note.image_url)
            try:
                send_mail('django-新note', new_note_email_message, from_email, to_email)
            except:
                pass
        return self.get_success_url()

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return redirect('/note/')

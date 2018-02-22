#!/usr/bin/env python
# coding=utf-8

from ..models import Category, Tag, Post
from django import template
from django.db.models.aggregates import Count
from django.utils.safestring import mark_safe
register = template.Library()

@register.assignment_tag
def get_future():
    return Post.objects.exclude(status=1).order_by('-created_time')
@register.assignment_tag
def get_invisible():
    return Post.objects.exclude(visible=True).order_by('-created_time')

@register.assignment_tag
def get_recent(app='blog', num=5):
    if app == 'blog':
        app = Post
    return app.objects.filter(visible=True, status=1).order_by('-created_time')[:num]

@register.assignment_tag
def get_categories(app='blog'):
    if app == 'blog':
        app = 'post'
    return Category.objects.annotate(num=Count(app)).filter(num__gt=0)

@register.assignment_tag
def get_archives(app='blog'):
    if app == 'blog':
        app = Post
    time_list = app.objects.dates('created_time', 'month', order='DESC')
    arch = []
    for time in time_list:
        num = app.objects.filter(created_time__year=time.year, created_time__month=time.month).count()
        arch.append({'date': time, 'num':num})
    return arch

@register.assignment_tag
def get_tags(app='blog'):
    if app == 'blog':
        app = 'post'
    return Tag.objects.annotate(num=Count(app)).filter(num__gt=0)



TEMP1 = """
<div class='comment'>
<span>%s評論說:</span><br>
    <span>%s</span>
"""



TEMP2 = """
<div class='col s11 offset-s%s'>
<span>%s 回復 %s:</span><br>
    <span>%s</span>
"""

def generate_comment_html(parent_comment, sub_comment_dic, margin_left_val):
    html = '<div class="comment">'
    for k, v_dic in sub_comment_dic.items():
        # 因为是子评论了，所以需要加上margin_left_val（30）像素的偏移量，子子评论再加margin_left_val（30）的偏移量，以此类推。
        html += TEMP2 % (margin_left_val, k.name, parent_comment.name, k.text)

        # 只要有字典，就递归的往下执行generate_comment_html()函数
        if v_dic:
            html += generate_comment_html(k, v_dic, margin_left_val)
        html += "</div>"
    html += "</div>"
    return html


@register.assignment_tag
def tree(comment_dic):
    # 将comment_dic字典里的数据拼接成html传给前端
    html = '<div class="comment">'
    for k, v in comment_dic.items():
        # 因为是根评论，所以margin-left应该是0，所以这里传入（0，k[1]），k[1]是评论内容
        html += TEMP1 % (k.name, k.text)
        # 如果v不为空字典，则执行generate_comment_html()
        if v:
            html += generate_comment_html(k, v, 1)
        html += "</div>"
    html += '</div>'

    return mark_safe(html)

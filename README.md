## django-myblog
### 简介
基于Django和MaterialDesign风格的个人blog.<br>
django版本:[django1.8](https://docs.djangoproject.com/en/1.8/)<br>
前端主要是[materializecss](https://github.com/Dogfalo/materialize)<br>
图标:[Material icons](http://icon.okgoes.com/)<br>
使用了simditor和ckeditor富文本编辑器,简单的全文搜索<br>
最近应该没时间继续弄了,以后有时间再折腾
### 目前主要功能
#### blog部分
- blog主页浮动卡片式设计
- blog分类,标签
- 统计blog的浏览量
- 侧边栏功能,包括最近发布,分类,标签
- 登录用户评论blog以及回复评论,支持富文本
#### note部分
- 分享一句话或者漂亮的图片
- 登录用户即可发布和修改note
- 可以设置可见性,详情支持富文本编辑
- 浮动卡片式设计
- note点赞
#### 用户登录
- oauth登录,目前支持github登录
- 登录用户可以发布blog评论和note
- 好的登录体验,登录后返回登录之前浏览的页面
#### 管理员
- 可直接blog新建修改,不用到admin后台修改
- 更方便的修改blog的分类,标签,修改blog时间
- 设置blog的可见性,指定blog的状态(草稿/发布),禁止评论blog
- 屏蔽或者删除不当的评论和note,
- 网站发生错误时邮件通知管理员

### 部署安装
参见[django部署:nginx+virtualenv+uwsgi+supervisor](https://www.huazhaozhe.info/blog/post/2)


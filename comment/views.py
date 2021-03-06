from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm
# Create your views here.

def update_comment(request):
    '''referer = request.META.get('HTTP_REFERER', reverse('home')) # 获取上一个网页信息，否则获取首页信息(reverse:根据别名）
                # 数据检查
                if not request.user.is_authenticated:
                    return render(request, 'error.html', {'message': '用户未登录', 'redirect_to': referer})
                text = request.POST.get('text', '').strip()
                if text == '':
                    return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})
                try:
                    content_type = request.POST.get('content_type', '')
                    object_id = int(request.POST.get('object_id', ''))
                    model_class = ContentType.objects.get(model=content_type).model_class() # 获取内容类型的模块
                    model_object = model_class.objects.get(pk=object_id) # 在这相当于Blog.objects.get
                except Exception as e:
                    return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})
            
                # 检查通过， 保存数据
                comment = Comment()
                comment.user = request.user
                comment.text = text
                comment.content_object = model_object
                comment.save()
            
                return redirect(referer)'''
    referer = request.META.get('HTTP_REFERER', reverse('home')) # 获取上一个网页信息，否则获取首页信息(reverse:根据别名）            
    comment_form = CommentForm(request.POST, user=request.user) # 把user对象传递到CommentForm里，在其内部设置继承来获取user
    data = {}
    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent #如果parent有顶级评论则添加其parent的顶级评论，否则添加parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 返回数据
        
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
        #return redirect(referer)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0]
        #return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
    return JsonResponse(data)
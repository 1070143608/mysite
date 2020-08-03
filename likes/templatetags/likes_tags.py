from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord
# 这个文件可直接在模板页面使用
register = template.Library()

@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.liked_num

@register.simple_tag(takes_context=True) # 这个表示可以传回前端模板页面的信息
def get_like_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj) # 获取的是contenttype类型，如<ContentType: blog>
    return content_type.model



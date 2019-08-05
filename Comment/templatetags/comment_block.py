from django import template

from Comment.forms import CommentForm
from Comment.models import Comment

register = template.Library()

@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target':target,
        'comment_form':CommentForm(),
        'comment_list':Comment.get_by_target(target),
    }
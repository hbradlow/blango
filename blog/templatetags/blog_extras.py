from django.contrib.auth import get_user_model
user_model = get_user_model()

from django import template
register = template.Library()

from blog.models import Post

from django.utils.safestring import mark_safe
from django.utils.html import escape, format_html

@register.filter
def author_details(author: user_model, current_user: user_model = None) -> str:
  if not isinstance(author, user_model):
    return ""

  if author == current_user:
    return format_html("<strong>me</strong>")

  if author.first_name and author.last_name:
    name = f"{author.first_name} {author.last_name}"
  else:
    name = f"{author.username}"

  if author.email:
    prefix = format_html("<a href=\"mailto:{}\">", author.email)
    suffix = format_html("</a>")
  else:
    prefix = ""
    suffix = ""

  return format_html("{}{}{}", prefix, name, suffix)

@register.simple_tag
def row(extra_classes=""):
  return format_html("<div class=\"row {}\">", extra_classes)

@register.simple_tag
def endrow():
    return format_html("</div>")

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk).order_by("-published_at")[:5]
  print(posts)
  return {"posts": posts, "title": "Recent Posts"}
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View

from post.models import Post

from .models import Comment
from .forms import CommentForm


class CommentCreateView(View):

    @staticmethod
    def post(request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        post = Post.objects.get(pk=kwargs['object_id'])
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.text = form.cleaned_data['text']
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
        messages.add_message(request, messages.ERROR, 'Не удалось оставить комментарий')
        return HttpResponseRedirect(post.get_absolute_url())

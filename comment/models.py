from django.contrib.auth.models import User
from django.db import models
from post.models import Post


class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Пост')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField(auto_now=True)

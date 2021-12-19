import json

from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async

from comment.models import Comment
from post.models import Post


class CommentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_proup_name = f'post_{self.post_id}'

        await self.channel_layer.group_add(
            self.post_proup_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.post_proup_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        comment = text_data_json['text']

        new_comment = await self.create_new_comment(comment)
        data = {
            'author': new_comment.author.username,
            'created_at': new_comment.created_at.strftime('%Y-%m-%d %H:%m'),
            'text': new_comment.text
        }
        await self.channel_layer.group_send(
            self.post_proup_name,
            {
                'type': 'new_comment',
                'message': data
            }
        )

    async def new_comment(self, event):
        message = event['message']

        await self.send(
            text_data=json.dumps({
                'message': message
            })
        )

    @database_sync_to_async
    def create_new_comment(self, text):
        post = Post.objects.get(pk=self.post_id)
        new_comment = Comment.objects.create(author=self.scope['user'],
                                             text=text,
                                             post=post)

        return new_comment

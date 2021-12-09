from tortoise import Model
from tortoise import fields


class Emotion(Model):
    id = fields.IntField(index=True, pk=True)
    name = fields.CharField(max_length=100)

    class Meta:
        table = "extra_emotion"


class Comment(Model):
    id = fields.IntField(pk=True, index=True)
    emoji = fields.JSONField(null=True)
    is_done = fields.BooleanField()
    emotion_text_type_id = fields.IntField(null=True)
    post_id = fields.IntField()
    comment_id = fields.CharField(max_length=50)
    commentator_login = fields.CharField(max_length=255)
    commentator_social_id = fields.CharField(max_length=255)
    text = fields.TextField()
    created_at = fields.DatetimeField()
    is_contain_profanity = fields.BooleanField()

    class Meta:
        table = "comment_emotion"

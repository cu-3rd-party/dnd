from tortoise import fields

from .base import TimestampedModel, UuidModel


class Campaign(TimestampedModel, UuidModel):
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=1023, default="")
    icon = fields.UUIDField(null=True)
    verified = fields.BooleanField(default=0)

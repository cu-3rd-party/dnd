from tortoise import fields, models

from .base import TimestampedModel, UuidModel


class Campaign(TimestampedModel, UuidModel):
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=1023, default="")
    icon = fields.CharField(max_length=1023, default="")
    verified = fields.BooleanField(default=0)

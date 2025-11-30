from tortoise import fields, models

from .base import TimestampedModel, CharacterData, UuidModel


class Character(TimestampedModel, CharacterData, UuidModel):
    user = fields.ForeignKeyField("models.User")
    campaign = fields.ForeignKeyField("models.Campaign")

    class Meta:
        unique_together = ("user", "campaign")

import logging

from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment

from db.models.base import CharacterData as BaseCharacterData
from db.models.character import Character
from db.models.user import User
from utils.character import CharacterData, parse_character_data

logger = logging.getLogger(__name__)


async def update_char_data(holder: BaseCharacterData, data: dict):
    holder.data = data
    await holder.save()


def character_preview_getter(user: User | Character, data: dict, *, light: bool = False):
    ret = {}
    info: CharacterData = parse_character_data(data)
    ret["character_data_preview"] = info.light_preview() if light else info.preview()
    avatar_url = data.get("avatar", {}).get("webp")
    if avatar_url:
        ret["avatar"] = MediaAttachment(
            url=avatar_url,
            type=ContentType.PHOTO,
        )
    else:
        logger.warning("No avatar for user %d", user.id)

    return ret

import logging

from aiogram import Bot
from aiogram.types import BufferedInputFile, InputFile
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.manager.message_manager import MessageManager

from services.settings import settings

logger = logging.getLogger(__name__)


def ensure_bucket(name: str) -> None:
    if settings.minio.bucket_exists(name):
        return
    settings.minio.make_bucket(name)
    logger.info("Created bucket %s", name)


class MinioMessageManager(MessageManager):
    async def get_media_source(
        self,
        media: MediaAttachment,
        bot: Bot,
    ) -> InputFile | str:
        if media.path and media.path.startswith("minio://"):
            bucket_name, object_name = media.path.replace("minio://", "").split(":")

            result = settings.minio.get_object(bucket_name, object_name)
            data = result.read()

            return BufferedInputFile(file=data, filename=media.path)
        return await super().get_media_source(media, bot)

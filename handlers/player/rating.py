import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, Multi

from db.models import User
from states.player_preview import PlayerPreview
from states.rating import AcademyRating

logger = logging.getLogger(__name__)
router = Router()


async def rating_getter(dialog_manager: DialogManager, **kwargs):
    top_users = await User.all().order_by("-rating")

    # Добавляем позиции в рейтинге
    top_with_positions = [(i + 1, user) for i, user in enumerate(top_users)]

    return {
        "top_with_positions": top_with_positions,
        "has_users": len(top_with_positions) > 0,
    }


async def on_preview(c: CallbackQuery, b: Select, m: DialogManager, user_id: int):
    await m.start(PlayerPreview.preview, data={"user_id": user_id, "light": True})


rating_dialog = Dialog(
    Window(
        Multi(
            Const("🏆 Рейтинг игроков"),
            Const(""),
            Const("Топ игроков по рейтингу в академии:"),
            Const(""),
            Const("📭 В рейтинге пока нет игроков", when=lambda data, *_: not data.get("has_users", False)),
            sep="\n",
        ),
        ScrollingGroup(
            Select(
                Format("{item[0]}. @{item[1].username} - {item[1].rating} ⭐"),
                id="preview",
                items="top_with_positions",
                item_id_getter=lambda x: x[1].id,
                on_click=on_preview,
                type_factory=int,
            ),
            hide_on_single_page=True,
            width=1,
            height=6,
            id="top",
            when="has_users",
        ),
        Cancel(Const("⬅️ Назад")),
        getter=rating_getter,
        state=AcademyRating.rating,
    ),
)

router.include_router(rating_dialog)

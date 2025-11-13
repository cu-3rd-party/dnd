from aiogram import Router
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Cancel, ListGroup
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery

from .states import ManageCharacters


# === Гетеры ===
async def get_characters_data(dialog_manager: DialogManager, **kwargs):
    mock_characters = [
        {"id": 1, "name": "Гарри Поттер", "level": 5, "house": "Гриффиндор"},
        {"id": 2, "name": "Гермиона Грейнджер", "level": 6, "house": "Гриффиндор"},
        {"id": 3, "name": "Драко Малфой", "level": 5, "house": "Слизерин"},
    ]
    return {
        "characters": mock_characters,
        "campaign_title": dialog_manager.dialog_data.get("selected_campaign", {}).get(
            "title", "Группа"
        ),
    }


# === Кнопки ===
async def on_add_character(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await callback.answer(
        "Функция добавления студента будет реализована в следующем обновлении",
        show_alert=True,
    )


async def on_remove_character(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await callback.answer(
        "Студент будет удален в следующем обновлении", show_alert=True
    )


# === Окна ===
manage_characters_window = Window(
    Format(
        "👥 Управление персонажами группы: {campaign_title}\n\n" "Список персонажей:"
    ),
    ListGroup(
        Button(
            Format("🎓 {item[name]} (Ур. {item[level]}, {item[house]})"),
            id="character",
            on_click=on_remove_character,
        ),
        id="characters_list",
        item_id_getter=lambda item: str(item["id"]),
        items="characters",
    ),
    Button(
        Const("➕ Добавить персонажа"), id="add_character", on_click=on_add_character
    ),
    Cancel(Const("⬅️ Назад")),
    state=ManageCharacters.main,
    getter=get_characters_data,
)

# === Создание диалога и роутера ===
dialog = Dialog(manage_characters_window)
router = Router()
router.include_router(dialog)

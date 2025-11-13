from aiogram import Router
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Cancel, ListGroup
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery

from . import states as campaign_states


# === Гетеры ===
async def get_permissions_data(dialog_manager: DialogManager, **kwargs):
    mock_users = [
        {
            "id": 1,
            "name": "Альбус Дамблдор",
            "permission": "Владелец",
            "status": "активен",
        },
        {
            "id": 2,
            "name": "Минерва Макгонагалл",
            "permission": "Редактор",
            "status": "активен",
        },
        {
            "id": 3,
            "name": "Северус Снейп",
            "permission": "Участник",
            "status": "активен",
        },
    ]
    return {
        "users": mock_users,
        "campaign_title": dialog_manager.dialog_data.get("selected_campaign", {}).get(
            "title", "Группа"
        ),
    }


# === Кнопки ===
async def on_user_selected(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await callback.answer("Выбран пользователь", show_alert=True)


async def on_change_permission(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await callback.answer(
        "Изменение прав доступа будет реализовано в следующем обновлении",
        show_alert=True,
    )


# === Окна ===
permissions_window = Window(
    Format(
        "🔐 Управление правами доступа: {campaign_title}\n\n" "Список пользователей:"
    ),
    ListGroup(
        Button(
            Format("👤 {item[name]} - {item[permission]} ({item[status]})"),
            id="user",
            on_click=on_user_selected,
        ),
        id="users_list",
        item_id_getter=lambda item: str(item["id"]),
        items="users",
    ),
    Button(
        Const("✏️ Изменить права"),
        id="change_permission",
        on_click=on_change_permission,
    ),
    Cancel(Const("⬅️ Назад")),
    state=campaign_states.EditPermissions.main,
    getter=get_permissions_data,
)

# === Создание диалога и роутера ===
dialog = Dialog(permissions_window)
router = Router()
router.include_router(dialog)

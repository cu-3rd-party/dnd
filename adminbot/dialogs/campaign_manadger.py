from aiogram import Router
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Row,
    ScrollingGroup,
    Back,
    Cancel,
    Start,
    SwitchTo,
    Next,
)
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.input import TextInput
from aiogram.types import CallbackQuery, Message

from services.api_client import api_client
from . import states as campaign_states


# === Гетеры ===
async def get_campaigns_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data.get("user_id")  # type: ignore
    page = dialog_manager.dialog_data.get("page", 0)
    campaigns_per_page = 5

    # Получаем кампании из API
    campaigns = await api_client.get_campaigns(user_id=user_id)

    if not campaigns:
        return {
            "campaigns": [],
            "current_page": 1,
            "total_pages": 1,
            "has_prev": False,
            "has_next": False,
            "has_campaigns": False,
        }

    start_idx = page * campaigns_per_page
    end_idx = start_idx + campaigns_per_page
    current_campaigns = campaigns[start_idx:end_idx]

    total_pages = (len(campaigns) + campaigns_per_page - 1) // campaigns_per_page

    return {
        "campaigns": current_campaigns,
        "current_page": page + 1,
        "total_pages": total_pages,
        "has_prev": page > 0,
        "has_next": end_idx < len(campaigns),
        "has_campaigns": len(campaigns) > 0,
    }


# === Кнопки ===
async def on_campaign_selected(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str
):
    # Сохраняем выбранную кампанию
    dialog_manager.dialog_data["selected_campaign_id"] = item_id

    # Находим кампанию в данных
    campaigns_data = await get_campaigns_data(
        callback.message, dialog_manager  # type: ignore
    )
    selected_campaign = next(
        (
            camp
            for camp in campaigns_data["campaigns"]
            if str(camp.get("id")) == item_id
        ),
        None,
    )

    if selected_campaign:
        dialog_manager.dialog_data["selected_campaign"] = selected_campaign

    await dialog_manager.switch_to(campaign_states.CampaignManage.main)


async def on_page_change(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    direction: int,
):
    current_page = dialog_manager.dialog_data.get("page", 0)
    campaigns_data = await get_campaigns_data(callback.message, dialog_manager)  # type: ignore
    total_pages = campaigns_data["total_pages"]

    new_page = current_page + direction
    if 0 <= new_page < total_pages:
        dialog_manager.dialog_data["page"] = new_page
        await dialog_manager.update({})


async def get_campaign_manage_data(dialog_manager: DialogManager, **kwargs):
    campaign = dialog_manager.dialog_data.get("selected_campaign", {})
    return {
        "campaign_title": campaign.get("title", "Неизвестная группа"),
        "campaign_description": campaign.get("description", "Описание отсутствует"),
        "campaign_id": campaign.get("id", "N/A"),
    }


# === Окна ===

# Главное окно списка кампаний
campaign_list_window = Window(
    Multi(
        Const("🏰 Магическая Академия - Управление учебными группами\n\n"),
        Format("Страница {current_page}/{total_pages}\n"),
    ),
    # Список кампаний
    Group(
        *[
            Button(
                Format("📚 {item.title}"),
                id=f"campaign_{i}",
                on_click=on_campaign_selected,  # type: ignore
            )
            for i in range(10)  # Максимум 10 кнопок
        ],
        id="campaigns_group",
        width=2,
        when="has_campaigns",
    ),
    Const(
        "У вас пока нет учебных групп",
        when=lambda data, widget, manager: not data.get("has_campaigns", False),
    ),
    # Навигация и действия
    Group(
        Row(
            Button(
                Const("⬅️"),
                id="prev_page",
                on_click=lambda c, b, d: on_page_change(c, b, d, -1),
                when="has_prev",
            ),
            Button(
                Const("➡️"),
                id="next_page",
                on_click=lambda c, b, d: on_page_change(c, b, d, 1),
                when="has_next",
            ),
        ),
        Button(
            Const("➕ Создать новую"),
            id="create_campaign",
            on_click=lambda c, b, d: d.start(
                campaign_states.CreateCampaign.select_title
            ),
        ),
        width=2,
    ),
    state=campaign_states.CampaignManagerMain.main,
    getter=get_campaigns_data,
)

# Окно управления конкретной кампанией
campaign_manage_window = Window(
    Format(
        "🎓 Управление группой: {campaign_title}\n\n"
        "Описание: {campaign_description}\n"
        "ID группы: {campaign_id}\n\n"
        "Выберите действие:"
    ),
    Group(
        Button(Const("✏️ Редактировать информацию"), id="edit_info"),
        Button(Const("👥 Управление студентами"), id="manage_students"),
        Button(Const("🔐 Настройки доступа"), id="permissions"),
        Button(Const("📊 Статистика группы"), id="stats"),
        width=1,
    ),
    Row(Back(Const("⬅️ Назад к списку")), Cancel(Const("❌ Закрыть"))),
    state=campaign_states.CampaignManage.main,
    getter=get_campaign_manage_data,
)

campaign_manager_dialogs = Dialog(campaign_list_window), Dialog(campaign_manage_window)

router = Router()

router.include_routers(*campaign_manager_dialogs)

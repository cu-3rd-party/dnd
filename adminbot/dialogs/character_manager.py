from datetime import datetime
from aiogram import Router
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import (
    Button,
    Back,
    # Cancel,
    ListGroup,
    Select,
    Group,
    # Row,
    Column,
)
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram.types import CallbackQuery  # , Message

from services.api_client import api_client
from . import states as campaign_states

# === ГЕТЕРЫ ===


async def get_characters_data(dialog_manager: DialogManager, **kwargs):
    """Получение данных о персонажах кампании через API"""
    campaign = dialog_manager.dialog_data.get("selected_campaign", {})
    campaign_id = campaign.get("id")

    if not campaign_id:
        return {
            "characters": [],
            "campaign_title": "Неизвестная группа",
            "total_characters": 0,
            "active_characters": 0,
            "average_level": 0,
        }

    # Получаем персонажей через API
    characters = await api_client.get_campaign_characters(campaign_id)

    # Обрабатываем данные персонажей
    processed_characters = []
    total_level = 0
    active_characters = 0

    for char in characters:
        # Извлекаем данные из поля data
        char_data = char.get("data", {})
        status = char_data.get("status", "активен")

        processed_char = {
            "id": char.get("id"),
            "name": char_data.get("name", "Безымянный"),
            "level": char_data.get("level", 1),
            "class": char_data.get("class", "⚔️ Воин"),
            "race": char_data.get("race", "Неизвестно"),
            "player": char_data.get("player", f"Игрок {char.get('owner_id', '?')}"),
            "status": status,
            "hp_current": char_data.get("hp_current", 10),
            "hp_max": char_data.get("hp_max", 10),
            "xp": char_data.get("xp", 0),
            "last_activity": char_data.get("last_activity", "Неизвестно"),
        }
        processed_characters.append(processed_char)
        total_level += processed_char["level"]

        if status == "активен":
            active_characters += 1

    average_level = (
        total_level / len(processed_characters) if processed_characters else 0
    )

    return {
        "characters": processed_characters,
        "campaign_title": campaign.get("title", "Группа"),
        "campaign_id": campaign_id,
        "total_characters": len(processed_characters),
        "active_characters": active_characters,
        "average_level": round(average_level, 1),
    }


async def get_character_detail_data(dialog_manager: DialogManager, **kwargs):
    """Получение детальной информации о персонаже через API"""
    selected_character_id = dialog_manager.dialog_data.get("selected_character_id")

    if not selected_character_id:
        return {
            "character": {
                "name": "Персонаж не выбран",
                "level": 0,
                "class": "Неизвестно",
                "race": "Неизвестно",
                "player": "Неизвестно",
                "status": "неактивен",
                "hp_current": 0,
                "hp_max": 0,
                "xp": 0,
                "last_activity": "Неизвестно",
            },
            "campaign_title": "Неизвестная группа",
        }

    # Получаем данные персонажа через API
    character_data = await api_client.get_character(int(selected_character_id))

    if not character_data:
        return {
            "character": {
                "name": "Персонаж не найден",
                "level": 0,
                "class": "Неизвестно",
                "race": "Неизвестно",
                "player": "Неизвестно",
                "status": "неактивен",
                "hp_current": 0,
                "hp_max": 0,
                "xp": 0,
                "last_activity": "Неизвестно",
            },
            "campaign_title": dialog_manager.dialog_data.get(
                "selected_campaign", {}
            ).get("title", "Группа"),
        }

    # Обрабатываем данные персонажа
    char_data = character_data.get("data", {})
    character = {
        "id": character_data.get("id"),
        "name": char_data.get("name", "Безымянный"),
        "level": char_data.get("level", 1),
        "class": char_data.get("class", "⚔️ Воин"),
        "race": char_data.get("race", "Неизвестно"),
        "player": char_data.get(
            "player", f"Игрок {character_data.get('owner_id', '?')}"
        ),
        "status": char_data.get("status", "активен"),
        "hp_current": char_data.get("hp_current", 10),
        "hp_max": char_data.get("hp_max", 10),
        "xp": char_data.get("xp", 0),
        "last_activity": char_data.get("last_activity", "Неизвестно"),
    }

    # Дополнительные вычисляемые поля
    hp_current = character["hp_current"]
    hp_max = character["hp_max"]
    hp_percentage = (hp_current / hp_max) * 100 if hp_max > 0 else 0
    hp_bar = "█" * int(hp_percentage / 10) + "░" * (10 - int(hp_percentage / 10))

    return {
        "character": character,
        "campaign_title": dialog_manager.dialog_data.get("selected_campaign", {}).get(
            "title", "Группа"
        ),
        "hp_percentage": int(hp_percentage),
        "hp_bar": hp_bar,
        "next_level_xp": character["level"] * 1000 + 1000,
        "xp_progress": (character["xp"] % 1000) / 10 if character["xp"] > 0 else 0,
    }


# === КНОПКИ ===


async def on_character_selected(
    callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str
):
    """Обработчик выбора персонажа"""
    dialog_manager.dialog_data["selected_character_id"] = item_id
    await dialog_manager.switch_to(campaign_states.ManageCharacters.view_character)


async def on_edit_character(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Обработчик редактирования персонажа"""
    selected_character_id = dialog_manager.dialog_data.get("selected_character_id")

    if not selected_character_id:
        await callback.answer("❌ Сначала выберите персонажа", show_alert=True)
        return

    character_data = await api_client.get_character(int(selected_character_id))
    if not character_data:
        await callback.answer("❌ Персонаж не найден", show_alert=True)
        return

    character_name = character_data.get("data", {}).get("name", "Безымянный")
    await callback.answer(
        f"✏️ Редактирование персонажа '{character_name}' будет доступно в следующем "
        "обновлении",
        show_alert=True,
    )


async def on_character_status_toggle(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Обработчик изменения статуса персонажа через API"""
    selected_character_id = dialog_manager.dialog_data.get("selected_character_id")

    if not selected_character_id:
        await callback.answer("❌ Сначала выберите персонажа", show_alert=True)
        return

    character_data = await api_client.get_character(int(selected_character_id))
    if not character_data:
        await callback.answer("❌ Персонаж не найден", show_alert=True)
        return

    char_data = character_data.get("data", {})
    current_status = char_data.get("status", "активен")
    new_status = "неактивен" if current_status == "активен" else "активен"

    # Обновляем статус через API
    update_data = {"status": new_status}
    result = await api_client.update_character(int(selected_character_id), update_data)

    if "error" in result:
        await callback.answer(
            f"❌ Ошибка при изменении статуса: {result['error']}", show_alert=True
        )
    else:
        await callback.answer(
            f"✅ Статус персонажа изменен на: {new_status}", show_alert=True
        )
        await dialog_manager.update({})


async def on_add_character(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Обработчик добавления нового персонажа через API"""
    campaign = dialog_manager.dialog_data.get("selected_campaign", {})
    campaign_id = campaign.get("id")

    if not campaign_id:
        await callback.answer("❌ Не выбрана кампания", show_alert=True)
        return

    # Создаем нового персонажа через API
    character_data = {
        "name": "Новый студент",
        "level": 1,
        "class": "🎓 Студент",
        "race": "Человек",
        "player": f"Студент {callback.from_user.first_name}",
        "hp_current": 10,
        "hp_max": 10,
        "xp": 0,
        "status": "активен",
        "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    result = await api_client.upload_character(
        owner_id=callback.from_user.id, campaign_id=campaign_id, data=character_data
    )

    if "error" in result:
        await callback.answer(
            f"❌ Ошибка при создании персонажа: {result['error']}", show_alert=True
        )
    else:
        character_name = result.get("data", {}).get("name", "Новый студент")
        await callback.answer(
            f"✅ Персонаж '{character_name}' создан!", show_alert=True
        )
        await dialog_manager.update({})


async def on_character_stats(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Обработчик просмотра статистики персонажа"""
    selected_character_id = dialog_manager.dialog_data.get("selected_character_id")

    if not selected_character_id:
        await callback.answer("❌ Сначала выберите персонажа", show_alert=True)
        return

    character_data = await get_character_detail_data(dialog_manager)
    character = character_data["character"]

    # Формируем детальную статистику
    stats_text = (
        f"📊 Детальная статистика: {character['name']}\n\n"
        f"🎯 Уровень: {character['level']}\n"
        f"⚔️ Класс: {character['class']}\n"
        f"👤 Раса: {character['race']}\n"
        f"❤️ Здоровье: {character['hp_current']}/{character['hp_max']}\n"
        f"⭐ Опыт: {character['xp']}\n"
        f"👥 Игрок: {character['player']}\n"
        f"🟢 Статус: {character['status']}\n"
        f"📅 Активность: {character['last_activity']}\n\n"
        f"🏰 Кампания: {character_data['campaign_title']}"
    )

    await callback.answer(stats_text, show_alert=True)


# === ОКНА ===

# Главное окно списка персонажей
characters_main_window = Window(
    Multi(
        Format("👥 Управление персонажами: {campaign_title}\n\n"),
        Format("Всего персонажей: {total_characters}\n"),
        Format("Активных: {active_characters}\n"),
        Format("Средний уровень: {average_level}\n\n"),
        Const("Список персонажей:"),
    ),
    ListGroup(
        Button(
            Format(
                "🎭 {item[name]} - ур. {item[level]} {item[class]}\n"
                "👤 {item[player]} | {item[status]}"
            ),
            id="character_select",
            on_click=on_character_selected,  # type: ignore
        ),
        id="characters_list",
        item_id_getter=lambda item: str(item["id"]),
        items="characters",
    ),
    Group(
        Button(
            Const("➕ Добавить персонажа"),
            id="add_character",
            on_click=on_add_character,
        ),
        width=1,
    ),
    Back(Const("⬅️ Назад к кампании")),
    state=campaign_states.ManageCharacters.main,
    getter=get_characters_data,
)

# Окно детального просмотра персонажа
character_detail_window = Window(
    Multi(
        Format("🎭 Детали персонажа: {character[name]}\n\n"),
        Format("🎯 Уровень: {character[level]}\n"),
        Format("⚔️ Класс: {character[class]}\n"),
        Format("👤 Раса: {character[race]}\n"),
        Format("👥 Игрок: {character[player]}\n"),
        Format("🟢 Статус: {character[status]}\n\n"),
        Format("❤️ Здоровье: {character[hp_current]}/{character[hp_max]}\n"),
        Format("   {hp_bar} {hp_percentage}%\n\n"),
        Format("⭐ Опыт: {character[xp]}\n"),
        Format("📊 До след. уровня: {xp_progress:.1f}% ({next_level_xp} XP)\n\n"),
        Format("📅 Последняя активность: {character[last_activity]}"),
    ),
    Column(
        Button(
            Const("✏️ Редактировать"), id="edit_character", on_click=on_edit_character
        ),
        Button(
            Const("📊 Подробная статистика"),
            id="character_stats",
            on_click=on_character_stats,
        ),
        Button(
            Format(
                "🔄 {character[status]=='активен' and 'Деактивировать' or 'Активировать'}"
            ),
            id="toggle_status",
            on_click=on_character_status_toggle,
        ),
    ),
    Back(Const("⬅️ Назад к списку")),
    state=campaign_states.ManageCharacters.view_character,
    getter=get_character_detail_data,
)

# === СОЗДАНИЕ ДИАЛОГА ===

characters_dialog = Dialog(
    characters_main_window,
    character_detail_window,
)

# Роутер для character_manager
character_router = Router()
character_router.include_router(characters_dialog)

# from aiogram_dialog import Dialog, StartMode, Window, DialogManager, SubManager
# from aiogram_dialog.widgets.kbd import Button, Group, Row, Back, Cancel, Next, ListGroup
# from aiogram_dialog.widgets.text import Const, Format, Multi
# from aiogram_dialog.widgets.input import TextInput
# from aiogram.types import CallbackQuery, Message

# from services.api_client import api_client
# from . import states as campaign_states


# # === Гетеры ===
# async def get_campaigns_data(dialog_manager: DialogManager, **kwargs):
#     user_id = dialog_manager.start_data.get("user_id")  # type: ignore
#     page = dialog_manager.dialog_data.get("page", 0)
#     campaigns_per_page = 5

#     # Получаем кампании из API
#     campaigns = await api_client.get_campaigns(user_id=user_id)

#     if not campaigns:
#         return {
#             "campaigns": [],
#             "current_page": 1,
#             "total_pages": 1,
#             "has_prev": False,
#             "has_next": False,
#             "has_campaigns": False,
#         }

#     start_idx = page * campaigns_per_page
#     end_idx = start_idx + campaigns_per_page
#     current_campaigns = campaigns[start_idx:end_idx]

#     total_pages = (len(campaigns) + campaigns_per_page - 1) // campaigns_per_page

#     return {
#         "campaigns": current_campaigns,
#         "current_page": page + 1,
#         "total_pages": total_pages,
#         "has_prev": page > 0,
#         "has_next": end_idx < len(campaigns),
#         "has_campaigns": len(campaigns) > 0,
#     }


# async def get_create_campaign_data(dialog_manager: DialogManager, **kwargs):
#     return {
#         "title": dialog_manager.dialog_data.get("title", "Не задано"),
#         "description": dialog_manager.dialog_data.get("description", "Не задано"),
#         "icon": dialog_manager.dialog_data.get("icon", "🏰"),  # Значок по умолчанию
#     }


# # === Кнопки ===
# async def on_campaign_selected(
#     callback: CallbackQuery, button: Button, dialog_manager: SubManager
# ):
#     # Сохраняем выбранную кампанию
#     dialog_manager.dialog_data["selected_campaign_id"] = dialog_manager.item_id

#     # Находим кампанию в данных
#     campaigns_data = await get_campaigns_data(dialog_manager)
#     selected_campaign = next(
#         (
#             camp
#             for camp in campaigns_data["campaigns"]
#             if str(camp.get("id")) == dialog_manager.item_id
#         ),
#         None,
#     )

#     if selected_campaign:
#         dialog_manager.dialog_data["selected_campaign"] = selected_campaign

#     await dialog_manager.start(campaign_states.CampaignManage.main)


# async def on_page_change(
#     callback: CallbackQuery,
#     button: Button,
#     dialog_manager: DialogManager,
#     direction: int,
# ):
#     current_page = dialog_manager.dialog_data.get("page", 0)
#     campaigns_data = await get_campaigns_data(
#         callback.message, dialog_manager  # type: ignore
#     )
#     total_pages = campaigns_data["total_pages"]

#     new_page = current_page + direction
#     if 0 <= new_page < total_pages:
#         dialog_manager.dialog_data["page"] = new_page
#         await dialog_manager.update({})


# async def get_campaign_manage_data(dialog_manager: DialogManager, **kwargs):
#     campaign = dialog_manager.dialog_data.get("selected_campaign", {})
#     return {
#         "campaign_title": campaign.get("title", "Неизвестная группа"),
#         "campaign_description": campaign.get("description", "Описание отсутствует"),
#         "campaign_id": campaign.get("id", "N/A"),
#     }


# async def on_campaign_title_entered(
#     message: Message, widget: TextInput, dialog_manager: DialogManager, text: str
# ):
#     if len(text) > 255:
#         await message.answer("Название слишком длинное (максимум 255 символов)")
#         return
#     dialog_manager.dialog_data["title"] = text
#     await dialog_manager.next()


# async def on_campaign_description_entered(
#     message: Message, widget: TextInput, dialog_manager: DialogManager, text: str
# ):
#     if len(text) > 1023:
#         await message.answer("Описание слишком длинное (максимум 1023 символа)")
#         return
#     dialog_manager.dialog_data["description"] = text
#     await dialog_manager.next()


# async def on_icon_selected(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     icon = {
#         "castle": "🏰",
#         "books": "📚",
#         "lightning": "⚡",
#         "fire": "🔥",
#         "moon": "🌙",
#         "star": "⭐",
#     }[button.widget_id or "castle"]
#     dialog_manager.dialog_data["icon"] = icon
#     await dialog_manager.next()


# async def on_create_cancel(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     await dialog_manager.done()
#     # Возвращаемся к списку кампаний
#     await dialog_manager.start(
#         campaign_states.CampaignManagerMain.main,
#         mode=StartMode.RESET_STACK,
#         data=dialog_manager.start_data,
#     )


# async def on_campaign_confirm(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     # Получаем данные из dialog_data
#     title = dialog_manager.dialog_data.get("title")
#     description = dialog_manager.dialog_data.get("description")
#     icon = dialog_manager.dialog_data.get("icon", "🏰")

#     # Получаем telegram_id пользователя
#     user_id = callback.from_user.id

#     if not title:
#         await callback.answer("Ошибка: не указано название")  # type: ignore
#         return

#     # Создаем кампанию через API
#     result = await api_client.create_campaign(
#         telegram_id=user_id, title=title, description=description, icon=icon
#     )

#     if "error" in result:
#         await callback.answer(
#             f"Ошибка при создании: {result['error']}", show_alert=True
#         )
#     else:
#         await callback.answer("🎉 Учебная группа успешно создана!", show_alert=True)
#         await dialog_manager.done()


# # === Окна ===

# # Главное окно списка кампаний
# campaign_list_window = Window(
#     Multi(
#         Const("🏰 Магическая Академия - Управление учебными группами\n\n"),
#         Format("Страница {current_page}/{total_pages}\n"),
#     ),
#     # Список кампаний
#     ListGroup(
#         *[
#             Button(
#                 Format("{item[icon]} {item[title]}"),
#                 id="campaign",
#                 on_click=on_campaign_selected,  # type: ignore
#             )
#         ][:10],
#         id="campaigns_group",
#         item_id_getter=lambda item: item["id"],
#         items="campaigns",
#         when="has_campaigns",
#     ),
#     Const(
#         "У вас пока нет учебных групп",
#         when=lambda data, widget, manager: not data.get("has_campaigns", False),
#     ),
#     # Навигация и действия
#     Group(
#         Row(
#             Button(
#                 Const("⬅️"),
#                 id="prev_page",
#                 on_click=lambda c, b, d: on_page_change(c, b, d, -1),
#                 when="has_prev",
#             ),
#             Button(
#                 Const("➡️"),
#                 id="next_page",
#                 on_click=lambda c, b, d: on_page_change(c, b, d, 1),
#                 when="has_next",
#             ),
#         ),
#         Button(
#             Const("➕ Создать новую"),
#             id="create_campaign",
#             on_click=lambda c, b, d: d.start(
#                 campaign_states.CreateCampaign.select_title
#             ),
#         ),
#         width=2,
#     ),
#     state=campaign_states.CampaignManagerMain.main,
#     getter=get_campaigns_data,
# )

# # Окно управления конкретной кампанией
# campaign_manage_window = Window(
#     Format(
#         "🎓 Управление группой: {campaign_title}\n\n"
#         "Описание: {campaign_description}\n"
#         "ID группы: {campaign_id}\n\n"
#         "Выберите действие:"
#     ),
#     Group(
#         Button(Const("✏️ Редактировать информацию"), id="edit_info"),
#         Button(Const("👥 Управление студентами"), id="manage_students"),
#         Button(Const("🔐 Настройки доступа"), id="permissions"),
#         Button(Const("📊 Статистика группы"), id="stats"),
#         width=1,
#     ),
#     Row(Back(Const("⬅️ Назад к списку")), Cancel(Const("❌ Закрыть"))),
#     state=campaign_states.CampaignManage.main,
#     getter=get_campaign_manage_data,
# )
# # Окно ввода названия
# title_window = Window(
#     Const(
#         "🏰 Создание новой учебной группы\n\n"
#         "Введите название для вашей учебной группы:\n"
#         "(максимум 255 символов)"
#     ),
#     TextInput(
#         id="campaign_title_input", on_success=on_campaign_title_entered  # type: ignore
#     ),
#     Cancel(Const("❌ Отмена")),
#     state=campaign_states.CreateCampaign.select_title,
# )
# # Окно ввода описания
# description_window = Window(
#     Multi(
#         Const("📝 Теперь введите описание для вашей группы:\n"),
#         Format("Название: {title}\n"),
#         Const("(максимум 1023 символа, можно пропустить)"),
#     ),
#     TextInput(
#         id="campaign_description_input",
#         on_success=on_campaign_description_entered,  # type: ignore
#     ),
#     Button(Const("⏭ Пропустить"), id="skip_description", on_click=Next()),
#     Back(Const("⬅️ Назад")),
#     state=campaign_states.CreateCampaign.select_description,
#     getter=get_create_campaign_data,
# )
# # Окно выбора иконки
# icon_window = Window(
#     Multi(
#         Const("🎨 Выберите иконку для вашей группы:\n"),
#         Format("Название: {title}\n"),
#         Format("Описание: {description}"),
#     ),
#     Group(
#         Button(Const("🏰 Замок"), id="castle", on_click=on_icon_selected),
#         Button(Const("📚 Книги"), id="books", on_click=on_icon_selected),
#         Button(Const("⚡ Молния"), id="lightning", on_click=on_icon_selected),
#         Button(Const("🔥 Огонь"), id="fire", on_click=on_icon_selected),
#         Button(Const("🌙 Луна"), id="moon", on_click=on_icon_selected),
#         Button(Const("⭐ Звезда"), id="star", on_click=on_icon_selected),
#         width=2,
#     ),
#     Button(Const("⏭ Пропустить"), id="skip_icon", on_click=Next()),
#     Back(Const("⬅️ Назад")),
#     state=campaign_states.CreateCampaign.select_icon,
#     getter=get_create_campaign_data,
# )
# # Окно подтверждения
# confirm_window = Window(
#     Multi(
#         Const("✅ Проверьте данные новой учебной группы:\n\n"),
#         Format("🎨 Иконка: {icon}"),
#         Format("📝 Название: {title}"),
#         Format("📄 Описание: {description}\n"),
#         Const("Всё верно?"),
#     ),
#     Button(
#         Const("✅ Создать группу"), id="confirm_create", on_click=on_campaign_confirm
#     ),
#     Back(Const("⬅️ Назад")),
#     Button(Const("❌ Отмена"), id="cancel_create", on_click=on_create_cancel),
#     state=campaign_states.CreateCampaign.confirm,
#     getter=get_create_campaign_data,
# )

# campaign_manager_dialogs = Dialog(campaign_list_window), Dialog(campaign_manage_window)
# create_campaign_dialog = Dialog(
#     title_window, description_window, icon_window, confirm_window
# )

# # router = Router()

# # router.include_routers(*campaign_manager_dialogs, create_campaign_dialog)

# from aiogram import Router
# from aiogram_dialog import Dialog, StartMode, Window, DialogManager, SubManager
# from aiogram_dialog.widgets.kbd import (
#     Button,
#     Group,
#     Row,
#     Back,
#     Cancel,
#     Next,
#     ListGroup,
#     Select,
#     Column,
# )
# from aiogram_dialog.widgets.text import Const, Format, Multi
# from aiogram_dialog.widgets.input import TextInput
# from aiogram.types import CallbackQuery, Message

# from services.api_client import api_client
# from . import states as campaign_states

# # === Дополнительные геттеры ===


# async def get_campaign_edit_data(dialog_manager: DialogManager, **kwargs):
#     campaign = dialog_manager.dialog_data.get("selected_campaign", {})
#     return {
#         "campaign_title": campaign.get("title", "Неизвестная группа"),
#         "campaign_description": campaign.get("description", "Описание отсутствует"),
#         "campaign_icon": campaign.get("icon", "🏰"),
#         "campaign_id": campaign.get("id", "N/A"),
#     }


# async def get_students_data(dialog_manager: DialogManager, **kwargs):
#     # Заглушка - в реальности будем получать из API
#     campaign_id = dialog_manager.dialog_data.get("selected_campaign", {}).get("id")
#     mock_students = [
#         {"id": 1, "name": "Гарри Поттер", "level": 5, "house": "Гриффиндор"},
#         {"id": 2, "name": "Гермиона Грейнджер", "level": 6, "house": "Гриффиндор"},
#         {"id": 3, "name": "Драко Малфой", "level": 5, "house": "Слизерин"},
#     ]
#     return {
#         "students": mock_students,
#         "campaign_title": dialog_manager.dialog_data.get("selected_campaign", {}).get(
#             "title", "Группа"
#         ),
#     }


# async def get_permissions_data(dialog_manager: DialogManager, **kwargs):
#     # Заглушка данных о правах доступа
#     mock_users = [
#         {
#             "id": 1,
#             "name": "Альбус Дамблдор",
#             "permission": "Владелец",
#             "status": "активен",
#         },
#         {
#             "id": 2,
#             "name": "Минерва Макгонагалл",
#             "permission": "Редактор",
#             "status": "активен",
#         },
#         {
#             "id": 3,
#             "name": "Северус Снейп",
#             "permission": "Участник",
#             "status": "активен",
#         },
#     ]
#     return {
#         "users": mock_users,
#         "campaign_title": dialog_manager.dialog_data.get("selected_campaign", {}).get(
#             "title", "Группа"
#         ),
#     }


# # === Обработчики для управления кампанией ===


# async def on_edit_info(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     await dialog_manager.start(campaign_states.EditCampaignInfo.select_field)


# async def on_manage_students(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     await dialog_manager.start(campaign_states.ManageStudents.main)


# async def on_permissions(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     await dialog_manager.start(campaign_states.EditPermissions.main)


# async def on_stats(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     campaign = dialog_manager.dialog_data.get("selected_campaign", {})
#     stats_text = (
#         f"📊 Статистика группы: {campaign.get('title', 'Неизвестная')}\n\n"
#         f"👥 Количество студентов: 12\n"
#         f"📚 Активных заданий: 5\n"
#         f"⭐ Средний уровень: 4.2\n"
#         f"🏆 Лучший студент: Гарри Поттер\n\n"
#         f"📈 Прогресс группы: 78%"
#     )
#     await callback.answer(stats_text, show_alert=True)


# # === Обработчики для редактирования информации ===


# async def on_field_selected(
#     callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str
# ):
#     field_map = {
#         "title": campaign_states.EditCampaignInfo.edit_title,
#         "description": campaign_states.EditCampaignInfo.edit_description,
#         "icon": campaign_states.EditCampaignInfo.edit_icon,
#     }
#     if item_id in field_map:
#         await dialog_manager.switch_to(field_map[item_id])


# async def on_title_edited(
#     message: Message, widget: TextInput, dialog_manager: DialogManager, text: str
# ):
#     if len(text) > 255:
#         await message.answer("Название слишком длинное (максимум 255 символов)")
#         return

#     # Обновляем данные в dialog_data
#     if "selected_campaign" not in dialog_manager.dialog_data:
#         dialog_manager.dialog_data["selected_campaign"] = {}
#     dialog_manager.dialog_data["selected_campaign"]["title"] = text

#     await dialog_manager.switch_to(campaign_states.EditCampaignInfo.confirm)


# async def on_description_edited(
#     message: Message, widget: TextInput, dialog_manager: DialogManager, text: str
# ):
#     if len(text) > 1023:
#         await message.answer("Описание слишком длинное (максимум 1023 символа)")
#         return

#     if "selected_campaign" not in dialog_manager.dialog_data:
#         dialog_manager.dialog_data["selected_campaign"] = {}
#     dialog_manager.dialog_data["selected_campaign"]["description"] = text

#     await dialog_manager.switch_to(campaign_states.EditCampaignInfo.confirm)


# async def on_icon_selected_edit(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     icon_map = {
#         "castle_edit": "🏰",
#         "books_edit": "📚",
#         "lightning_edit": "⚡",
#         "fire_edit": "🔥",
#         "moon_edit": "🌙",
#         "star_edit": "⭐",
#     }
#     icon = icon_map.get(button.widget_id, "🏰")

#     if "selected_campaign" not in dialog_manager.dialog_data:
#         dialog_manager.dialog_data["selected_campaign"] = {}
#     dialog_manager.dialog_data["selected_campaign"]["icon"] = icon

#     await dialog_manager.switch_to(campaign_states.EditCampaignInfo.confirm)


# async def on_edit_confirm(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     # Здесь будет вызов API для сохранения изменений
#     campaign = dialog_manager.dialog_data.get("selected_campaign", {})
#     await callback.answer(
#         f"✅ Изменения для {campaign.get('title')} сохранены!", show_alert=True
#     )
#     await dialog_manager.back()


# # === Обработчики для управления студентами ===


# async def on_add_student(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     await callback.answer(
#         "Функция добавления студента будет реализована в следующем обновлении",
#         show_alert=True,
#     )


# async def on_remove_student(
#     callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str
# ):
#     await callback.answer(
#         f"Студент {item_id} будет удален в следующем обновлении", show_alert=True
#     )


# # === Обработчики для управления правами ===


# async def on_user_selected(
#     callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str
# ):
#     dialog_manager.dialog_data["selected_user_id"] = item_id
#     await callback.answer(f"Выбран пользователь {item_id}", show_alert=True)


# async def on_change_permission(
#     callback: CallbackQuery, button: Button, dialog_manager: DialogManager
# ):
#     await callback.answer(
#         "Изменение прав доступа будет реализовано в следующем обновлении",
#         show_alert=True,
#     )


# # === Диалоги для управления кампанией ===

# # Редактирование информации о кампании
# edit_campaign_dialog = Dialog(
#     Window(
#         Format(
#             "✏️ Редактирование группы: {campaign_title}\n\n"
#             "Выберите что хотите изменить:"
#         ),
#         Column(
#             Button(Const("📝 Название группы"), id="title", on_click=on_field_selected),
#             Button(
#                 Const("📄 Описание группы"),
#                 id="description",
#                 on_click=on_field_selected,
#             ),
#             Button(Const("🎨 Иконка группы"), id="icon", on_click=on_field_selected),
#         ),
#         Back(Const("⬅️ Назад")),
#         Cancel(Const("❌ Отмена")),
#         state=campaign_states.EditCampaignInfo.select_field,
#         getter=get_campaign_edit_data,
#     ),
#     Window(
#         Const("Введите новое название группы:"),
#         TextInput(id="edit_title_input", on_success=on_title_edited),
#         Back(Const("⬅️ Назад")),
#         state=campaign_states.EditCampaignInfo.edit_title,
#     ),
#     Window(
#         Const("Введите новое описание группы:"),
#         TextInput(id="edit_description_input", on_success=on_description_edited),
#         Back(Const("⬅️ Назад")),
#         state=campaign_states.EditCampaignInfo.edit_description,
#     ),
#     Window(
#         Const("Выберите новую иконку для группы:"),
#         Group(
#             Button(Const("🏰 Замок"), id="castle_edit", on_click=on_icon_selected_edit),
#             Button(Const("📚 Книги"), id="books_edit", on_click=on_icon_selected_edit),
#             Button(
#                 Const("⚡ Молния"), id="lightning_edit", on_click=on_icon_selected_edit
#             ),
#             Button(Const("🔥 Огонь"), id="fire_edit", on_click=on_icon_selected_edit),
#             Button(Const("🌙 Луна"), id="moon_edit", on_click=on_icon_selected_edit),
#             Button(Const("⭐ Звезда"), id="star_edit", on_click=on_icon_selected_edit),
#             width=2,
#         ),
#         Back(Const("⬅️ Назад")),
#         state=campaign_states.EditCampaignInfo.edit_icon,
#     ),
#     Window(
#         Format(
#             "✅ Проверьте изменения:\n\n"
#             "🎨 Иконка: {campaign_icon}\n"
#             "📝 Название: {campaign_title}\n"
#             "📄 Описание: {campaign_description}\n\n"
#             "Сохранить изменения?"
#         ),
#         Button(Const("✅ Сохранить"), id="save_changes", on_click=on_edit_confirm),
#         Back(Const("⬅️ Назад")),
#         Cancel(Const("❌ Отмена")),
#         state=campaign_states.EditCampaignInfo.confirm,
#         getter=get_campaign_edit_data,
#     ),
# )

# # Управление студентами
# manage_students_dialog = Dialog(
#     Window(
#         Format(
#             "👥 Управление студентами группы: {campaign_title}\n\n" "Список студентов:"
#         ),
#         ListGroup(
#             Button(
#                 Format("🎓 {item[name]} (Ур. {item[level]}, {item[house]})"),
#                 id="student",
#                 on_click=on_remove_student,
#             ),
#             id="students_list",
#             item_id_getter=lambda item: str(item["id"]),
#             items="students",
#         ),
#         Button(
#             Const("➕ Добавить студента"), id="add_student", on_click=on_add_student
#         ),
#         Back(Const("⬅️ Назад")),
#         state=campaign_states.ManageStudents.main,
#         getter=get_students_data,
#     ),
# )

# # Управление правами доступа
# permissions_dialog = Dialog(
#     Window(
#         Format(
#             "🔐 Управление правами доступа: {campaign_title}\n\n"
#             "Список пользователей:"
#         ),
#         ListGroup(
#             Button(
#                 Format("👤 {item[name]} - {item[permission]} ({item[status]})"),
#                 id="user",
#                 on_click=on_user_selected,
#             ),
#             id="users_list",
#             item_id_getter=lambda item: str(item["id"]),
#             items="users",
#         ),
#         Button(
#             Const("✏️ Изменить права"),
#             id="change_permission",
#             on_click=on_change_permission,
#         ),
#         Back(Const("⬅️ Назад")),
#         state=campaign_states.EditPermissions.main,
#         getter=get_permissions_data,
#     ),
# )

# # Обновим главное окно управления кампанией с правильными обработчиками
# campaign_manage_window = Window(
#     Format(
#         "🎓 Управление группой: {campaign_title}\n\n"
#         "Описание: {campaign_description}\n"
#         "ID группы: {campaign_id}\n\n"
#         "Выберите действие:"
#     ),
#     Group(
#         Button(
#             Const("✏️ Редактировать информацию"), id="edit_info", on_click=on_edit_info
#         ),
#         Button(
#             Const("👥 Управление студентами"),
#             id="manage_students",
#             on_click=on_manage_students,
#         ),
#         Button(
#             Const("🔐 Настройки доступа"), id="permissions", on_click=on_permissions
#         ),
#         Button(Const("📊 Статистика группы"), id="stats", on_click=on_stats),
#         width=1,
#     ),
#     Row(Back(Const("⬅️ Назад к списку")), Cancel(Const("❌ Закрыть"))),
#     state=campaign_states.CampaignManage.main,
#     getter=get_campaign_manage_data,
# )

# # Обновим router чтобы включить все диалоги
# # router = Router()
# # router.include_routers(
# #     Dialog(campaign_list_window),
# #     Dialog(campaign_manage_window),
# #     create_campaign_dialog,
# #     edit_campaign_dialog,
# #     manage_students_dialog,
# #     permissions_dialog,
# # )

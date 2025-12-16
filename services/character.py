import logging
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class CharacterStat(BaseModel):
    score: int = 0
    modifier: int = 0


class CharacterHP(BaseModel):
    current: int = 0
    max: int = 0
    temp: int = 0
    ac: int = 0
    speed: int = 0


class CharacterWeapon(BaseModel):
    name: str = "Неизвестно"
    mod: str = ""
    damage: str = ""
    notes: str = ""


class CharacterCoins(BaseModel):
    pp: int = 0
    gp: int = 0
    ep: int = 0
    sp: int = 0
    cp: int = 0


class CharacterData(BaseModel):
    name: str = "Неизвестно"
    klass: str = Field(default="Неизвестно", alias="class")
    subclass: str = ""
    level: int = 0
    race: str = "Неизвестно"
    background: str = "Неизвестно"
    alignment: str = "Неизвестно"
    avatar_link: str | None

    age: str = ""
    height: str = ""
    weight: str = ""
    eyes: str = ""
    skin: str = ""
    hair: str = ""

    proficiency: int = 0
    stats: dict[str, CharacterStat] = Field(default_factory=dict)

    skills: dict[str, dict] = Field(default_factory=dict)
    prof_skills: list[str] = Field(default_factory=list)

    hp: CharacterHP = Field(default_factory=CharacterHP)

    weapons: list[CharacterWeapon] = Field(default_factory=list)

    traits: str = ""
    equipment: str = ""
    background_story: str = ""
    personality: str = ""
    appearance: str = ""
    allies: str = ""
    proficiencies: str = ""

    coins: CharacterCoins = Field(default_factory=CharacterCoins)

    class Config:
        validate_by_name = True

    def preview(self) -> str:
        return (
            f"<b>Имя:</b> {self.name}\n"
            f"<b>Класс:</b> {self.klass} {f'({self.subclass})' if self.subclass else ''}\n"
            f"<b>Уровень:</b> {self.level}\n"
            f"<b>Хиты:</b> {self.hp.current}/{self.hp.max} {f'(+{self.hp.temp} временное)' if self.hp.temp else ''}\n"
            f"<b>Класс брони:</b> {self.hp.ac}\n"
            f"<b>Скорость:</b> {self.hp.speed} фт.\n"
            f"<b>Раса:</b> {self.race}\n"
            f"<b>Предыстория:</b> {self.background}\n"
            f"<b>Мировоззрение:</b> {self.alignment}"
        )

    def preview_stats(self) -> str:
        return "\n".join(
            [f"<b>{STATS_CONVERSION[key]}:</b> {value.score}({value.modifier})" for key, value in self.stats.items()]
        )


STATS_CONVERSION = {
    "str": "Сила",
    "dex": "Ловкость",
    "con": "Телосложение",
    "int": "Интеллект",
    "wis": "Мудрость",
    "cha": "Харизма",
}


def parse_character_data(data: dict) -> CharacterData:
    """
    Превращает json персонажа Long Story Short в адекватный Pydantic объект
    """
    basic_info = data.get("info", {})
    sub_info = data.get("subInfo", {})
    vitality = data.get("vitality", {})
    coins_data = data.get("coins", {})
    prof_skills = []
    for skill_name, skill_data in data.get("skills", {}).items():
        if skill_data.get("isProf"):
            prof_skills.append(skill_name)
    stats = {}
    for stat_name, stat_data in data.get("stats", {}).items():
        stats[stat_name] = CharacterStat(
            score=stat_data.get("score", 0),
            modifier=stat_data.get("modifier", 0),
        )
    weapons = [
        CharacterWeapon(
            name=weapon.get("name", {}).get("value", "Неизвестно"),
            mod=weapon.get("mod", {}).get("value", ""),
            damage=weapon.get("dmg", {}).get("value", ""),
            notes=weapon.get("notes", {}).get("value", ""),
        )
        for weapon in data.get("weaponsList", [])
    ]

    # noinspection PyArgumentList
    return CharacterData(
        # Basic info
        name=data.get("name", {}).get("value", "Неизвестно"),
        klass=basic_info.get("charClass", {}).get("value", "Неизвестно"),
        subclass=basic_info.get("charSubclass", {}).get("value", ""),
        level=basic_info.get("level", {}).get("value", 0),
        race=basic_info.get("race", {}).get("value", "Неизвестно"),
        background=basic_info.get("background", {}).get("value", "Неизвестно"),
        alignment=basic_info.get("alignment", {}).get("value", "Неизвестно"),
        avatar_link=basic_info.get("avatar", {}).get("webp") or basic_info.get("avatar", {}).get("jpeg"),
        # Physical characteristics
        age=sub_info.get("age", {}).get("value", ""),
        height=sub_info.get("height", {}).get("value", ""),
        weight=sub_info.get("weight", {}).get("value", ""),
        eyes=sub_info.get("eyes", {}).get("value", ""),
        skin=sub_info.get("skin", {}).get("value", ""),
        hair=sub_info.get("hair", {}).get("value", ""),
        # Stats
        proficiency=data.get("proficiency", 0),
        stats=stats,
        # Skills
        skills=data.get("skills", {}),
        prof_skills=prof_skills,
        # Vitality
        hp=CharacterHP(
            current=vitality.get("hp-current", {}).get("value", 0),
            max=vitality.get("hp-max", {}).get("value", 0),
            temp=vitality.get("hp-temp", {}).get("value", 0),
            ac=vitality.get("ac", {}).get("value", 0),
            speed=vitality.get("speed", {}).get("value", 0),
        ),
        # Weapons
        weapons=weapons,
        # Text content
        traits=extract_telegram_text(data.get("text", {}).get("traits", {}).get("value", {})),
        equipment=extract_telegram_text(data.get("equipment", {}).get("value", {})),
        background_story=extract_telegram_text(data.get("quests", {}).get("value", {})),
        personality=extract_telegram_text(data.get("background", {}).get("value", {})),
        appearance=extract_telegram_text(data.get("appearance", {}).get("value", {})),
        allies=extract_telegram_text(data.get("allies", {}).get("value", {})),
        proficiencies=extract_telegram_text(data.get("prof", {}).get("value", {})),
        # Currency
        coins=CharacterCoins(
            pp=coins_data.get("pp", {}).get("value", 0),
            gp=coins_data.get("gp", {}).get("value", 0),
            ep=coins_data.get("ep", {}).get("value", 0),
            sp=coins_data.get("sp", {}).get("value", 0),
            cp=coins_data.get("cp", {}).get("value", 0),
        ),
    )


def extract_telegram_text(text_data: dict[str, Any]) -> str:
    """
    Превращает json документооборот в HTML
    """
    if not text_data:
        return ""

    content = text_data.get("data", {}).get("content", [])
    paragraphs = []

    for block in content:
        if block.get("type") == "paragraph":
            paragraph_text = process_paragraph(block.get("content", []))
            if paragraph_text:
                paragraphs.append(paragraph_text)

    return "\n".join(paragraphs)


def process_paragraph(items: list[dict[str, Any]]) -> str:
    """Process all items in paragraph into HTML."""
    result = []

    for item in items:
        item_type = item.get("type")

        if item_type == "text":
            html_text = process_text_item(item)
            if html_text:
                result.append(html_text)

        elif item_type == "roller":
            result.append(process_roller_item(item))

    return " ".join(result).strip()


def process_text_item(item: dict[str, Any]) -> str:
    """Apply HTML formatting to text item."""
    text = item.get("text", "").strip()
    if not text:
        return ""

    for mark in item.get("marks", []):
        mark_type = mark.get("type")
        if mark_type == "bold":
            text = f"<b>{text}</b>"
        elif mark_type == "italic":
            text = f"<i>{text}</i>"
        elif mark_type == "underline":
            text = f"<u>{text}</u>"

    return text


def process_roller_item(item: dict[str, Any]) -> str:
    """Convert roller item to placeholder HTML-like form."""
    roller_text = item.get("content", [{}])[0].get("text", "")
    return f"[{roller_text}]"

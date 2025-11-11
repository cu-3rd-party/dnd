import aiohttp
import logging
from typing import Optional, Dict, Any, List
from settings import settings

logger = logging.getLogger(__name__)


class DnDApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def ping(self) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/api/ping/") as response:
                return await response.json()

    async def get_campaigns(
        self, user_id: Optional[int] = None, campaign_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Получить кампании пользователя"""
        try:
            params = {}
            if user_id:
                params["user_id"] = user_id
            if campaign_id:
                params["campaign_id"] = campaign_id

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/campaign/get/", params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # API может вернуть один объект или массив
                        if isinstance(data, list):
                            return data
                        else:
                            return [data]
                    else:
                        logger.error(f"API error: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting campaigns: {e}")
            return []

    async def create_campaign(
        self,
        telegram_id: int,
        title: str,
        description: Optional[str] = None,
        icon: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Создать новую кампанию"""
        try:
            payload = {
                "telegram_id": telegram_id,
                "title": title,
                "description": description,
                "icon": icon,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/campaign/create/", json=payload
                ) as response:
                    if response.status == 201:
                        return await response.json()
                    else:
                        logger.error(f"API error creating campaign: {response.status}")
                        return {"error": f"API error: {response.status}"}
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            return {"error": str(e)}

    async def add_to_campaign(
        self, campaign_id: int, owner_id: int, user_id: int
    ) -> Dict[str, Any]:
        """Добавить пользователя в кампанию"""
        try:
            payload = {
                "campaign_id": campaign_id,
                "owner_id": owner_id,
                "user_id": user_id,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/campaign/add/", json=payload
                ) as response:
                    if response.status in [200, 201]:
                        return await response.json()
                    else:
                        logger.error(f"API error adding to campaign: {response.status}")
                        return {"error": f"API error: {response.status}"}
        except Exception as e:
            logger.error(f"Error adding to campaign: {e}")
            return {"error": str(e)}


# Инициализация клиента API
api_client = DnDApiClient(settings.BACKEND_URL)  # Замените на ваш URL

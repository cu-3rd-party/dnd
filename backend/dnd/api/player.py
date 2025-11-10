from django.http import HttpRequest
from django.http import HttpRequest
from ninja import Router

from ..models import Player
from ..schemas import (
    Message,
)
from ..schemas.player import RegisterRequest

router = Router()


@router.post(
    path="register/",
    response={
        200: Message,
        201: Message,
    },
)
def register_player(request: HttpRequest, player_request: RegisterRequest):
    _, created = Player.objects.update_or_create(
        telegram_id=player_request.telegram_id, defaults=player_request.dict()
    )
    if not created:
        return 200, Message(message="Player was already created")
    return 201, Message(message="Player created successfully")

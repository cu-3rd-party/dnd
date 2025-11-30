from ninja import Schema
from datetime import datetime


class InvitationCreateRequest(Schema):
    campaign_id: int
    invited_player_telegram_id: int
    invited_by_telegram_id: int


class InvitationByUsernameRequest(Schema):
    campaign_id: int
    username: str
    invited_by_telegram_id: int


class InvitationResponse(Schema):
    id: int
    campaign_id: int
    campaign_title: str
    invited_player_telegram_id: int
    invited_by_telegram_id: int
    status: str
    token: str
    expires_at: datetime
    created_at: datetime


class InvitationAcceptRequest(Schema):
    invitation_token: str
    character_id: int

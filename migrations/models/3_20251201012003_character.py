from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "character" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "data" JSONB NOT NULL,
    "id" UUID NOT NULL PRIMARY KEY,
    "campaign_id" UUID NOT NULL REFERENCES "campaign" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_character_user_id_c77625" UNIQUE ("user_id", "campaign_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "character";"""


MODELS_STATE = (
    "eJztmm1v2jAQx78KyqtO6ioaaOmmaRJQurGtZWphm1ZVkUkMWE0cljjrUMV339mJ85ysUN"
    "holzdtOd8l9u/88D/ce8WyDWy6B11kzRGZUuV17V6hyMLwR6Ztv6ag+Txq4QaGxqZw1uNe"
    "Y5c5SGdgnyDTxWAysKs7ZM6Izd9BPdPkRlsHR0Knkcmj5IeHNWZPMZthBxqub8BMqIF/YV"
    "d+nN9qE4JNI9FdYvB3C7vGFnNhG436p2fCk79urOm26Vk08p4v2MymobvnEeOAx/C2KabY"
    "QQwbsWHwXgYjlia/x2BgjofDrhqRwcAT5JkchvJm4lGdM6iJN/EfzbfKCnh0m3K0hDLO4n"
    "7pjyoas7Aq/FXd9+3LvcbxCzFK22VTRzQKIspSBCKG/FDBNQKpO5gPW0MsC/QUWhixcD7U"
    "ZGQKrhGEHsg/1oEsDRHlaIZJzBLfekwVGIMxoOYiyGAJ42H/vHc1bJ9/5iOxXPeHKRC1hz"
    "3eogrrImXd81Niw/rwF074kNrX/vB9jX+sfR9c9NKJC/2G3xXeJ+QxW6P2nYaM2GSTVgkG"
    "PKPEenNjzcQmI6vE/tPEBp2P8soIM3E2pd0ZcvLTGQakMgm4djR3FvqlmZhO2Qw+qkdHJc"
    "n70r4Umx94pTJyETSpftsyATHesxVQpsL+HlDlEedGEudhXW08gCd3KwTqNyaJEn01lNK/"
    "Yhgx/IkdAg/MkTYd2zYxovko42EpnGOI2xbP+lakTGcw+JTYiDv9YYrh6LzTA7oCLTgRJs"
    "z9iyHg5IJxchtTOtwwRvrtHXIMLdES00AwS0HBYsfNIR/Enn28xCYqWPlSPMvn7Oa+upQT"
    "R1rl8cIZ2apdRC3bZKlW2oIomope83fzN2WY5FUbcWAl5UbCbaP1xrXiuf5zw5rmpqpB1l"
    "m4VQ3yv0vVqgZ5ponN1CB8JWcz+uFqcFGgmwP/VB5HFIheG0Rn+zWTuOxmN/NYkjc+5ETK"
    "pMDbO29/S2u/7qdBJ50L/oBOSgbKk0hb7YBJhW3ypPmnjP94sMT2GzjLc6l1yLRPWcFWEw"
    "WlmHGJtJO0oEvw6+UrVW00Wmq9cXxy1Gy1jk7qJ+ArOpVtapWJ7v47Lp8T07VATydhZ0mf"
    "2Q6GSfgRLwTtPvQbUT3v+4dAA47cp6aXweygu1AQxicQDA8Ghf2KpNu+6rZPe0ru4t4Auf"
    "h39U+XXmrbyidYXMVts3YRUzOnbJFTtrhikWtj08WKz4g/XXTpUaVK2Z740O0wSOjjqpSn"
    "shfuVyXMc1e6VQnzTBNblTB/tYQJT6gM4eIbgXjMWrcCQdZLsG766EncCjTUB9wJNNTCGw"
    "HelKSIDIvkCMXSy4AwZms3ARuGWN0F7JI63+pdQBs7RJ8pOYo6aCnV1Cjy2Zl/OXpGAlo9"
    "bLaaJ43jZqibQ0uZXP6zNP4Ja2nFe/ZYSPVPC9FxAEtjBYiB+9MEeFivP+iGvV5ywV5PA4"
    "Q3MkxzhHyx7IuFVMqvSPmtcNBu/nhZ/gb8X7kl"
)

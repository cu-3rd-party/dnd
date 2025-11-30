from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "invite" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL PRIMARY KEY,
    "role" SMALLINT NOT NULL,
    "start_data" UUID NOT NULL,
    "campaign_id" UUID NOT NULL REFERENCES "campaign" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_invite_start_d_0286f9" ON "invite" ("start_data");
COMMENT ON COLUMN "invite"."role" IS 'На какую роль мы приглашаем пользователя';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "invite";"""


MODELS_STATE = (
    "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"
    "zL4vY="
)

from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "invite" ADD "created_by_id" BIGINT;
        ALTER TABLE "invite" ADD "used" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "invite" ADD CONSTRAINT "fk_invite_user_ccbb40fc" FOREIGN KEY ("created_by_id") REFERENCES "user" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "invite" DROP CONSTRAINT IF EXISTS "fk_invite_user_ccbb40fc";
        ALTER TABLE "invite" DROP COLUMN "created_by_id";
        ALTER TABLE "invite" DROP COLUMN "used";"""


MODELS_STATE = (
    "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"
)

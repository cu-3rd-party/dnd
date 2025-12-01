from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "rating" INT NOT NULL DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "rating";"""


MODELS_STATE = (
    "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"
)

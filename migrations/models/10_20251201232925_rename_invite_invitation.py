from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "invite" RENAME TO "invitation";
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
           ALTER TABLE "invitation" RENAME TO "invite"; """


MODELS_STATE = (
    "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"
)

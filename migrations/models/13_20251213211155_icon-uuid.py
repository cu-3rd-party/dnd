from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "campaign" ALTER COLUMN "icon" DROP DEFAULT;
        ALTER TABLE "campaign" ALTER COLUMN "icon" DROP NOT NULL;
        ALTER TABLE "campaign" ALTER COLUMN "icon" TYPE UUID USING "icon"::UUID;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "campaign" ALTER COLUMN "icon" TYPE VARCHAR(1023) USING "icon"::VARCHAR(1023);
        ALTER TABLE "campaign" ALTER COLUMN "icon" SET NOT NULL;
        ALTER TABLE "campaign" ALTER COLUMN "icon" SET DEFAULT '';"""


MODELS_STATE = (
    "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"
)

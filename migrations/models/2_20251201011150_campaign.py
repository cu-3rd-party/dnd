from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "campaign" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "description" VARCHAR(1023) NOT NULL DEFAULT '',
    "icon" VARCHAR(1023) NOT NULL DEFAULT '',
    "verified" BOOL NOT NULL DEFAULT False
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "campaign";"""


MODELS_STATE = (
    "eJztmH9P2kAcxt8K6V8ucaa2IGxZllBkk0VgUdgWjWmO3lEuttfaXqfE8N53d/3dQieg0x"
    "H+MfT7o3f3ea69xz5KtgOR5R91gO0CbBLpY+1RIsBG7Ecpd1iTgOumGR6gYGKJYiNbNfGp"
    "BwzK4lNg+YiFIPIND7sUO3wMElgWDzoGK8TETEMBwXcB0qljIjpDHktc37AwJhA9ID++dG"
    "/1KUYWzE0XQz62iOt07orYeNw7/SIq+XAT3XCswCZptTunM4ck5UGA4RHv4TkTEeQBimBm"
    "GXyW0YrjUDhjFqBegJKpwjQA0RQEFochfZoGxOAMamIk/qf+WVoDj+EQjhYTylk8LsJVpW"
    "sWUYkP1TlrXxyoJ+/EKh2fmp5ICiLSQjQCCsJWwTUFaXiIL1sHtAz0lGUottFyqPnOAlwY"
    "tR7FPzaBHAdSyukOizHH+DZjKrE1wCGx5pGCFYxHvX73ctTuf+crsX3/zhKI2qMuzygiOi"
    "9ED0JJHPZ8hA9OcpPaz97orMYva1fDQbcoXFI3upL4nEBAHZ049zqAmc0WR2MwrDIVNnDh"
    "hsLmO/fCvqqw0eRTXSmmFipL2pkBb7mcSUNBSYbrjWpngwfdQsSkM3apNBoV4v1oX4iXH6"
    "sqKDKIUkqYW+QgZme2BspC278DKm1xbuRxHsuK+gSevGwl0DCZJ4qN9VDG9XuGKcPfyMPs"
    "hkusjeY4FgJkOcpsWwHnhPW9FE/5RayMNhye517EWm9UYDjua11GV6BlRZiKcG8wYji5YZ"
    "zeZpwOD0yAcXsPPKiXMo7irKotp2zFLkYAAabAw9fJVxXZ6LEv7GzJXot4pbUO4opntdXX"
    "kQXmdxdTutnGaGvY7BG6htVmuhd3YXTSbeextzxnTD7K+w+KoqpNRVZPWo16s9loyS1WK6"
    "ZUTjWrtm7vK9+Euc0a7sq9Ad95n7Y34DsqbMmA8ye5rOi3y+FghWmM6gs6jgkjeg2xQQ9r"
    "FvbpzdvUsUI3vuScZLG7Oei3fxWNT+d8qBW14DfQCh4oOaHW8JLZno38ZKR6BdbnPnpyfl"
    "JVnuAmVWWll+SpPEUAbbzEjlfayKTnxTzkM0PceRfZZsbemC3zkVGm0kmCtObNfKLdIduo"
    "HNeb9ZZ6Uk/cYhKpMol/N4Ts3zl/ze8SmZb9R570JcgejTUgRuX/J8BjWX7SFwm54oOEXA"
    "TIRqSILLGvq81OpmXvd1b5nVc9XhZ/AE8v61I="
)

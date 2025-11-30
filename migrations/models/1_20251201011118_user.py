from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "data" JSONB NOT NULL,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(32),
    "admin" BOOL NOT NULL,
    CONSTRAINT "uid_user_id_df1604" UNIQUE ("id", "username")
);
CREATE INDEX IF NOT EXISTS "idx_user_usernam_9987ab" ON "user" ("username");
CREATE INDEX IF NOT EXISTS "idx_user_admin_0aee3c" ON "user" ("admin");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user";"""


MODELS_STATE = (
    "eJztVl1v2jAU/SuIp07qKgif2xswtjIVmFrYplZVZGITLBw7TZy2qOp/n6+TkA8gox0S29"
    "S35Nxz7XvPSez7VHYEJsw/m/rEK38sPZU5coh6yOCnpTJy3QQFQKIZ08QgZsx86SFLKmyO"
    "mE8UhIlvedSVVHCF8oAxAIWliJTbCRRwehcQUwqbyIWu4+amTDGsCqvrkm5v1RvlmDwSHw"
    "jw6i7NOSUMZwoP8zRuypWrsS61B1x+1lwoYWZaggUOT/juSi4EXydQLgG1CScekgR2kF4A"
    "PUHJUetxm2H5CSWsMpWDyRwFTKY02FMYS3AQVVXj6x5t2OX9B8Oo1VpGpdZsN+qtVqNdaS"
    "uuLmkz1HoOG04ECZfSsgy+DEYTaFQo50I7AXjWOUiiMEvrnQhseQQkMZHcFPqTikjqkO1S"
    "ZzNzkuMo9Sx+yBsQy13kQAwkFiTf4oE8UD3gMWeryN4CeSeDYf9q0hl+g04c379jWqLOpA"
    "8RQ6OrHHrSfJf1Y71I6cdgcl6C19L1eNTXCgpf2p7eMeFNrstQEwqkMLl4MBFOfYkxGguj"
    "mImxgYtfaWw2883YoxobFZ/4Cn/ypqNfr8aj7W7G/JyPU64UvcHUkqclRn15+3f6WOAbtJ"
    "yxbPS9c9k771yeDDs/c/aMehfjbt4LWKCrj8fUXxPfUBsK9xbI2/G/pHJyKqtW9tA1cr1A"
    "1kNfPQ56NBnhtlyo15pRoHKsac3ISxpFDB3KqoiwQ/mWi1sIRhDfruI6JyfhTCUd5ts8sI"
    "hFV/F4fJH5NLuD3MU8mg67/cuTqhZVkahM3dcwDc2XqesagBmylg/Iw+ZGRBhiF3cz5BhO"
    "HkEc2Vog6BO6iqbFDvGotdg2R0aRwkkSJZyDzpJ/Mjn+R2OjUa236u1as76eFtdI0ZD4+4"
    "Hwnng+lPSCAzCV8qrz7xjzQeYENBqNPY5Axdp5BupY7hBUv8YLRIzo/6aA1UplDwEVa6eA"
    "OpYVUO0oCd8yvu4edlIpb/POrnnnqNfL8y9TEEo6"
)

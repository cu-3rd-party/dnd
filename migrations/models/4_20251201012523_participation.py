from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "participation" (
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL PRIMARY KEY,
    "role" SMALLINT NOT NULL,
    "campaign_id" UUID NOT NULL REFERENCES "campaign" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_participati_user_id_c158e0" UNIQUE ("user_id", "campaign_id")
);
COMMENT ON COLUMN "participation"."role" IS 'PLAYER: 0\nMASTER: 1\nOWNER: 2';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "participation";"""


MODELS_STATE = (
    "eJztm21v2joUx78KyqtO6q1ooKWbrq4UKL3jjoeqwHbvugqZxIDVxMkSZx2q+O7Xdp4fB5"
    "S20PlNS47PSezfcezzL+6jZJga1J2TFjAsgOZY+lB5lDAwIP2QaTuuSMCyohZmIGCqc2c1"
    "7jV1iA1UQu0zoDuQmjToqDayCDLZM7Cr68xoqtQR4XlkcjH67sIJMeeQLKBNG27vqBlhDf"
    "6ETnBp3U9mCOpaortIY8/m9glZWtw2Hncur7gne9x0opq6a+DI21qShYlDd9dF2gmLYW1z"
    "iKENCNRiw2C99EccmLweUwOxXRh2VYsMGpwBV2cwpD9nLlYZgwp/EvtR/0vaAI9qYoYWYc"
    "JYPK68UUVj5laJPar1Ubk5qp2/46M0HTK3eSMnIq14ICDAC+VcI5CqDdmwJ4BkgV7SFoIM"
    "mA81GZmCq/mhJ8GHbSAHhohyNMMCzAG+7ZhKdAzaAOtLP4MljEedXns4UnrXbCSG43zXOS"
    "Jl1GYtMrcuU9YjLyUmfT+8Fye8SeVLZ/Sxwi4rXwf9djpxod/oq8T6BFxiTrD5MAFabLIF"
    "1gAM9YwS61ralolNRorEvmpi/c5HeSWI6DCb0tYC2PnpDANSmaS49jR3Bvg50SGekwW9lM"
    "/OSpL3Wbnhix/1SmWk7zfJXtsqATHesw1QpsJeDqj0hH0jifO0KtfW4MncCoF6jUmiSN0M"
    "ZeAvGEYMf0Ab0RvmlDZN09QhwPko42EpnFMa91w8q89SyjQHg25iIW52RimG416zTelytN"
    "QJEW7u9EcUJysYZ/exSocZpkC9fwC2Nkm0xGogOktpBQttJ4e8H3v16QbqoODND4rn4D77"
    "ua6ugokTWPO2FwvYBKnI4kN9Io/r+L0OjAmbN6ZsFs2kbJMhG2kLwGDOe82ezZ6UmSd5Ci"
    "w+iUokWMJtpxrsVnId776hzrsTumybxUzost+9fBe67I0mNrNxsjc5m9F/hoN+gZbw/VN5"
    "HGNK9FZDKjmu6Mghd/uZx5K8sSEnUhYUvUc95d90PdzqDprpXLAbNFOlcbATTTbbYFJhu9"
    "xpXpXxLzeW2HpD9/Jcak0072BSsNREQSlmrETaS1q0S/TXH+9luVZryNXa+cVZvdE4u6he"
    "UF/eqWxTo0yIdP5mkiIxXQs0RhJ2lvSVaUM6CT/BJafdof0GWM37m4xfA46dQ9MQ1GyDh7"
    "AgjE8gOjw6KOiptJYybCmXbSn35d4Bufj3F4dLL7Vs5RMsVrbPqV2Smi5Hv2REX7GGsTKu"
    "QscIHSN0zB6Wu0LHvNHEZnSMbeZ9vUQrxTZ2jcwunEhsEPrKJaN03VX+a998qFS/4Z4yHL"
    "GPp9/w4EuffeLA1y4na3LjPCwg2UVZyTjsKd2uVyMK7SK0i9Au+0VZaJffXLvwqZkjWYIp"
    "W6xUgndj1wLFY8Tuzrv0JHlStiauuxz6CX2aMjmUtfBYyJa3Xt0K2fJGEyu+fnnRr1/CHS"
    "pDuPiEVzxmq1NeftZLsO5660mc8qrJa5zxqsmFJ7xYU5Ii0AyUUyiWHu4KY57tZNeOIYqz"
    "XftUnYuzXS98tkuBNlIXUo7K8FuOy3QGiHz25t9q3pCokE/rjfpF7bweaonQUiYhfi0Xft"
    "D1ZcOz5LEQcTA/2iLpq7EBRN/9MAGeVqtrnSKvlhwir6YB0icSiHPETXEpHAsR1XBRNbxB"
    "8bH77WX1PzSkjzM="
)

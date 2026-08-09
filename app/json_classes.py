from pydantic import BaseModel, Field


class From(BaseModel):
    phone_number: str


class To(BaseModel):
    phone_number: str


class Payload(BaseModel):
    from_: From = Field(alias="from")
    text: str
    to: list[To]


class Data(BaseModel):
    event_type: str
    id: str
    occurred_at: str
    payload: Payload


class Root(BaseModel):
    data: Data

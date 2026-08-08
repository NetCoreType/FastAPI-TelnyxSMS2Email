from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    smtp_pass: str
    smtp_user: str
    smtp_host: str
    smtp_port: int
    smtp_from_address: str
    production: bool

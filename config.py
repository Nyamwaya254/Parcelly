from pydantic_settings import BaseSettings,SettingsConfigDict

_base_config = SettingsConfigDict(
        env_file ="./.env",
        env_ignore_empty=True,
        extra = "ignore"
    )

class SecuritySettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str 

    model_config = _base_config


    
security_settings = SecuritySettings()

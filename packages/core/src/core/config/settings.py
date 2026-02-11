"""Application settings loaded from environment variables."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings for the van assistant system.

    Settings are loaded from environment variables. Each field has a default
    value that can be overridden by setting the corresponding environment variable.
    """

    # --- Docker / Compose settings ---
    compose_project_name: str = Field(
        default="van-assistant",
        validation_alias="COMPOSE_PROJECT_NAME",
    )

    # --- MQTT credentials ---
    mqtt_username: str = Field(default="user1", validation_alias="MQTT_USERNAME")
    mqtt_password: str = Field(default="password1", validation_alias="MQTT_PASSWORD")

    # Optional defaults for convenience
    mqtt_host: str = Field(default="localhost", validation_alias="MQTT_HOST")
    mqtt_port: int = Field(default=1883, validation_alias="MQTT_PORT")


# --- usage ---
if __name__ == "__main__":
    settings = Settings()
    print("Settings:", settings.model_dump())

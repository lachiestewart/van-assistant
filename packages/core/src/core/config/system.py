"""System-level configuration."""

from pydantic import BaseModel


class SystemConfig(BaseModel):
    """System-level configuration."""

    name: str

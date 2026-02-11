"""Configuration parser for van-assistant system."""

import tomllib
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field

from core.config.devices import RenogyDeviceConfig, VictronDeviceConfig
from core.config.system import SystemConfig

DeviceUnion = Annotated[
    VictronDeviceConfig | RenogyDeviceConfig,
    Field(discriminator="brand"),
]


class VanConfig(BaseModel):
    """Main configuration object for the van assistant system."""

    system: SystemConfig
    devices: list[DeviceUnion] = Field(default_factory=list)


def load_config(config_path: str | Path = "van-config.toml") -> VanConfig:
    """Load van configuration from file.

    Args:
        config_path: Path to the configuration file. Defaults to "van-config.toml".

    Returns:
        VanConfig instance with parsed configuration.

    """
    config_path = Path(config_path)

    if not config_path.exists():
        msg = f"Configuration file not found: {config_path}"
        raise FileNotFoundError(msg)

    with config_path.open("rb") as f:
        data = tomllib.load(f)

    return VanConfig.model_validate(data)

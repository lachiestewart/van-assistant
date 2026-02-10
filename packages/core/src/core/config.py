"""Configuration parser for van-assistant system."""

import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class SystemConfig(BaseModel):
    """System-level configuration."""

    name: str


class DeviceConfig(BaseModel):
    """Configuration for a single device."""

    name: str
    connection: str | None = None


class DevicesConfig(BaseModel):
    """Configuration for all devices."""

    mppt: DeviceConfig | None = None
    dcdc: DeviceConfig | None = None
    charger: DeviceConfig | None = None


class VanConfig(BaseModel):
    """Main configuration object for the van assistant system."""

    system: SystemConfig
    devices: DevicesConfig = Field(default_factory=DevicesConfig)

    @classmethod
    def from_file(cls, config_path: str | Path) -> "VanConfig":
        """Load configuration from a TOML file.

        Args:
            config_path: Path to the TOML configuration file.

        Returns:
            VanConfig instance with parsed configuration.

        Raises:
            FileNotFoundError: If the config file doesn't exist.
            ValueError: If the config file is invalid.

        """
        config_path = Path(config_path)

        if not config_path.exists():
            msg = f"Configuration file not found: {config_path}"
            raise FileNotFoundError(msg)

        with config_path.open("rb") as f:
            data = tomllib.load(f)

        return cls.model_validate(data)

    def to_dict(self) -> dict:
        """Convert configuration to a dictionary.

        Returns:
            Dictionary representation of the configuration.

        """
        return self.model_dump(exclude_none=True)


def load_config(config_path: str | Path = "van-config.toml") -> VanConfig:
    """Load van configuration from file.

    Args:
        config_path: Path to the configuration file. Defaults to "van-config.toml".

    Returns:
        VanConfig instance with parsed configuration.

    """
    return VanConfig.from_file(config_path)

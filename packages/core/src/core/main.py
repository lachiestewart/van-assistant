"""Main entry point for core van assistant system."""

from shared.logger import get_logger

from core.config.config import load_config

logger = get_logger(__name__)


def main() -> None:
    """Run the van assistant system."""
    config = load_config()
    logger.info(f"Loaded configuration: {config}")

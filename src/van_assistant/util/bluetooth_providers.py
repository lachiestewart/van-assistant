import logging

import requests
import yaml

from van_assistant.devices.brands import SupportedBrand

logger = logging.getLogger(__name__)


url = "https://bitbucket.org/bluetooth-SIG/public/raw/main/assigned_numbers/company_identifiers/company_identifiers.yaml"


def get_company_identifiers() -> dict[int, str]:
    """Fetch Bluetooth company identifiers from the official Bluetooth SIG repository.

    Returns:
        A dictionary mapping company identifier values to company names.

    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    text = response.content.decode("utf-8", errors="replace")
    data = yaml.safe_load(text)
    ids = data["company_identifiers"]
    return {entry["value"]: entry["name"] for entry in ids}


COMPANY_IDS: dict[int, str] = get_company_identifiers()
COMPANY_IDS[0x3461] = "Remco Energy"


if __name__ == "__main__":
    company_identifiers = get_company_identifiers()
    logger.info(company_identifiers[0x02E1])
    for identifier, name in company_identifiers.items():
        if name == SupportedBrand.VICTRON:
            logger.info(f"{identifier}: {name}")

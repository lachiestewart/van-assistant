import requests
import yaml

from van_assistant.devices.base import SupportedBrand

url = "https://bitbucket.org/bluetooth-SIG/public/raw/main/assigned_numbers/company_identifiers/company_identifiers.yaml"


def get_company_identifiers() -> dict[int, str]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    text = response.content.decode("utf-8", errors="replace")
    data = yaml.safe_load(text)
    ids = data["company_identifiers"]
    return {entry["value"]: entry["name"] for entry in ids}


COMPANY_IDS: dict[int, str] = get_company_identifiers()


if __name__ == "__main__":
    company_identifiers = get_company_identifiers()
    print(company_identifiers[0x02E1])
    for identifier, name in company_identifiers.items():
        if name == SupportedBrand.VICTRON:
            print(f"{identifier}: {name}")

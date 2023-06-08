from json import loads
from typing import Union
from requests import get, post
from datetime import datetime as dt
from pandas import DataFrame, to_datetime


def get_metadata() -> dict[str, str]:
    with open("credentials/metadata.json") as cfile:
        credentials = loads(cfile.read())
    return credentials


def _is_valid_date(date_string: str) -> bool:
    if not isinstance(date_string, str):
        return False

    try:
        dt.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        pass
    try:
        dt.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        return True
    except ValueError:
        pass
    try:
        dt.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        return True
    except ValueError:
        pass

    return False

def _parse_arg(value: Union[str, tuple, int, float]) -> str:

    logic_map_date = {
        "<=": "[before]",
        "<": "[strictly_before]",
        ">=": "[after]",
        ">": "[strictly_after]",
    }
    logic_map_number = {
        "<=": "[lte]",
        "<": "[lt]",
        ">=": "[gte]",
        ">": "[gt]",
        "between": "[between]",
    }
    if isinstance(value, (tuple, list)):
        if _is_valid_date(value[1]):
            suffix = logic_map_date[value[0]]
            parsed_value = value[1]
        else:
            suffix = logic_map_number[value[0]]
            parsed_value = f"{value[1]}..{value[2]}" if value[0] == "between" else value[1]
    else:
        suffix = ""
        parsed_value = value

    return f"{suffix}={parsed_value}"

def _parse_args(**args) -> str:
    if not args:
        return ""
    return "?" + "&".join(f"{key}{_parse_arg(value)}" for key, value in args.items())

def get_all_credentials(env: str = "prod") -> DataFrame:
    path_type = "credentials"
    http_request = {
        "url": f"{API_URLS[env]}/{path_type}",
        "headers": {
            "X-API-Key": API_KEYS[env],
        }
    }
    http_response = get(**http_request)
    parsed_content = loads(http_response.text)
    return DataFrame(parsed_content["hydra:member"])


def get_credential(_id="credentials", env: str = "prod") -> DataFrame:
    path_type = "credentials"
    http_request = {
        "url": f"{API_URLS[env]}/{path_type}",
        "headers": {
            "X-API-Key": API_KEYS[env],
        }
    }
    response = get(**http_request)
    parsed_response = loads(response.text)
    return DataFrame(parsed_response["hydra:member"])


def get_invoices(rfc: str, env: str = "prod", **query_args) -> Union[DataFrame, None]:
    http_request = {
        "url": f"{API_URLS[env]}/taxpayers/{rfc}/invoices{_parse_args(**query_args)}",
        "headers": {
            "X-API-Key": API_KEYS[env],
        }
    }
    response = get(**http_request)

    if (response.status_code - 200) >= 100:
        raise ConnectionError

    parsed_response = response.json()

    if not parsed_response:
        return None
    elif parsed_response['hydra:totalItems'] == 0:
        return None

    return DataFrame(parsed_response["hydra:member"]).drop('@id', axis=1)


def retrieve_cfdi(invoice_id: str, format: str = "json", env: str = "prod") -> None:
    http_request = {
        "url": f"{API_URLS[env]}/invoices/{invoice_id}/cfdi",
        "headers": {
            "X-API-Key": API_KEYS[env],
            "Accept": ACCEPT_FORMAT[format],
        },
    }
    response = get(**http_request)

    with open(f"{invoice_id}.{format}", "wb") as file:
        file.write(response.content)

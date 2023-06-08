from json import loads

with open("../credentials/configuration.json") as config_file:
    info = loads(config_file.read())
    API_URLS = info["api_urls"]
    API_KEYS = info["api_keys"]


API_URLS = {
    "prod": "https://api.satws.com",
    "test": "https://api.sandbox.satws.com",
}
API_KEYS = {
    "prod": "3a5faf1c2155c2ded9ca82aafa1bfa49",
    "test": "",
}

ACCEPT_FORMAT = {
    "pdf": "application/pdf",
    "json": "application/json",
    "xml": "text/xml",
}
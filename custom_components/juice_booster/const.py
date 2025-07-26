DOMAIN = "juice_booster"
TOKEN_URL = "https://sso.jplus-pilot.com/auth/realms/juice/protocol/openid-connect/token"
USER_API = "https://profile.juice-pilot.com/api/v2/users/{user_id}"
DEVICE_API = "https://profile.juice-pilot.com/api/v2/devices/{device_id}"
CHARGING_API = "https://profile.juice-pilot.com/api/v2/charging-view/{device_id}"
CONTROL_API = "https://profile.juice-pilot.com/api/v2/devices/{device_id}/charges/maxSupplyCurrent"
AVAILABLE_AMPERES = [0, 6, 8, 10, 13, 16]

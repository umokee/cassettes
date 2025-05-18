from app.config import ROLE_PERMISSIONS


class AccessPolicy:
    def __init__(self, role: str):
        self._role = role.lower()
        self._config = ROLE_PERMISSIONS.get(self._role, {})

    def is_enabled(self, section: str) -> bool:
        return self._config.get(section, {}).get("enabled", False)

    def is_readonly(self, section: str) -> bool:
        return self._config.get(section, {}).get("readonly", True)

    def get_label(self, section: str) -> str:
        return self._config.get(section, {}).get("label", section)

import os

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "Cassettes"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "112211"),
    "host": os.getenv("DB_HOST", "192.168.1.118"),
    "port": os.getenv("DB_PORT", "5432"),
}

ROLE_PERMISSIONS = {
    "администратор": {
        "CassetteManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление кассетами",
        },
        "GenreManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление жанрами",
        },
        "FineManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление штрафами",
        },
        "ClientManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление клиентами",
        },
        "ClientStatusManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление статусами",
        },
        "EmployeeManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление сотрудниками",
        },
        "PositionManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление должностями",
        },
        "TariffTypeManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление типами тарифов",
        },
        "TariffManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Управление тарифами",
        },
        "RentalManagement": {
            "enabled": False,
            "readonly": False,
            "label": "Аренды",
        },
        "PenaltyAccountingManagement": {
            "enabled": False,
            "readonly": False,
            "label": "Штрафы",
        },
    },
    "кассир": {
        "CassetteManagement": {
            "enabled": True,
            "readonly": True,
            "label": "Кассеты",
        },
        "GenreManagement": {
            "enabled": False,
            "readonly": False,
            "label": "Жанры",
        },
        "FineManagement": {
            "enabled": True,
            "readonly": True,
            "label": "Штрафы",
        },
        "ClientManagement": {
            "enabled": True,
            "readonly": True,
            "label": "Клиенты",
        },
        "ClientStatusManagement": {
            "enabled": False,
            "readonly": False,
            "label": "Статусы клиентов",
        },
        "EmployeeManagement": {
            "enabled": False,
            "readonly": False,
            "label": "Сотрудники",
        },
        "PositionManagement": {
            "enabled": False,
            "readonly": False,
            "label": "Должности",
        },
        "TariffTypeManagement": {
            "enabled": False,
            "readonly": False,
            "label": "Типы",
        },
        "TariffManagement": {
            "enabled": True,
            "readonly": True,
            "label": "Тарифы",
        },
        "RentalManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Аренды",
        },
        "PenaltyAccountingManagement": {
            "enabled": True,
            "readonly": False,
            "label": "Начислить штраф",
        },
    },
}

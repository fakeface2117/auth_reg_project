import enum


class SexEnum(str, enum.Enum):
    """Маппинг для пола. Например в БД будет 'MAN', на бэке используется 'man' """
    MAN = "man"
    WOMAN = "woman"


class RoleEnum(str, enum.Enum):
    """В БД 'USER', на бэке 'user' """
    USER = "user"
    SELLER = "seller"
    ADMIN = "admin"


class OrderStatusEnum(str, enum.Enum):
    CREATED = "создан"
    IS_GOING_TO = "собирается"
    IN_DELIVERY = "в доставке"
    DELIVERED = "доставлен"
    PRESENTED = "вручен"
    CANCELED = "отменен"

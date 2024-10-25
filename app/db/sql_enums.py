import enum


class SexEnum(str, enum.Enum):
    MAN = "мужчина"
    WOMAN = "женщина"


class RoleEnum(str, enum.Enum):
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

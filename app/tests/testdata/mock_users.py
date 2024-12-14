from datetime import datetime

users_test_data = [
    {
        "email": "admin@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$SdbM6fkZf+qYek2Wxiz2vw$WKsf/oRKw2ojKOU7EfT23UukQEgocWVFLHp3NNVKwns",
        "role_id": 3,
        "is_active": True,
        "is_superuser": True,
        "is_verified": True,
        "first_name": "админ",
        "last_name": "админ",
        "birth_date": datetime.strptime("2000-01-01", "%Y-%m-%d"),
        "sex": "man",
        "contacts": [
            {
                "contact": "VK",
                "value": "vk_id_0"
            },
            {
                "contact": "PHONE",
                "value": "88005553535"
            }
        ]
    },
    {
        "email": "test@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$SdbM6fkZf+qYek2Wxiz2vw$WKsf/oRKw2ojKOU7EfT23UukQEgocWVFLHp3NNVKwns",
        "role_id": 1,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "first_name": "Райан",
        "last_name": "Госслинг",
        "birth_date": datetime.strptime("2000-01-01", "%Y-%m-%d"),
        "sex": "man",
        "contacts": [
            {
                "contact": "VK",
                "value": "vk_id_1"
            },
            {
                "contact": "PHONE",
                "value": "88005553534"
            }
        ]
    }
]

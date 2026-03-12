from shop_api.redis_client import redis_client

CODE_TTL = 300  # 5 минут


def save_code(email, code):
    redis_client.setex(f"code:{email}", CODE_TTL, code)


def get_code(email):
    return redis_client.get(f"code:{email}")


def delete_code(email):
    redis_client.delete(f"code:{email}")






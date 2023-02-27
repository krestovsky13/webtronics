from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class Hasher:
    """
    Класс хеширования паролей
    """

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

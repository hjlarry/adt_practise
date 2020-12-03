import random
import base64

IDENTITY_PASSWORD = bytearray(range(256))


class InvalidPasswordErr(Exception):
    pass


def validatePwd(pwd: bytearray) -> bool:
    return len(pwd) == 256 and len(set(pwd)) == 256


def loadsPwd(pwd: str) -> bytearray:
    try:
        pwd = base64.urlsafe_b64decode(pwd.encode("utf8", errors="strict"))
        pwd = bytearray(pwd)
    except:
        raise InvalidPasswordErr

    if not validatePwd(pwd):
        raise InvalidPasswordErr

    return pwd


def dumpsPwd(pwd: bytearray) -> str:
    if not validatePwd(pwd):
        raise InvalidPasswordErr
    return base64.urlsafe_b64encode(pwd).decode("utf8", errors="strict")


def randomPwd() -> bytearray:
    pwd = IDENTITY_PASSWORD.copy()
    random.shuffle(pwd)
    return pwd


class Cipher:
    def __init__(self, encodePwd: bytearray, decodePwd: bytearray) -> None:
        self.encodePwd = encodePwd.copy()
        self.decodePwd = decodePwd.copy()

    def encode(self, bs: bytearray) -> None:
        for i, v in enumerate(bs):
            bs[i] = self.encodePwd[v]

    def decode(self, bs: bytearray) -> None:
        for i, v in enumerate(bs):
            bs[i] = self.decodePwd[v]

    @classmethod
    def NewCipher(cls, encodePwd: bytearray) -> Cipher:
        decodePwd = encodePwd.copy()
        for i, v in enumerate(encodePwd):
            decodePwd[v] = i
        return cls(encodePwd, decodePwd)
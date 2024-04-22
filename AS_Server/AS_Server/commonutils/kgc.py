from .utils import *
from fastecdsa import curve, keys, point


class KGC:
    """KGC"""

    def __init__(self, ec_curve=curve.secp256k1):
        self.ec_curve = ec_curve
        self.s = None
        self.Ppub = None

    def set_up(self) -> None:
        self.s = keys.gen_private_key(self.ec_curve)
        self.Ppub = keys.get_public_key(self.s, self.ec_curve)

    def get_Ppub(self) -> str:
        return point2hex(self.Ppub)

    def get_s(self) -> str:
        return int2hex(self.s)

    def get_q(self) -> str:
        return int2hex(self.ec_curve.q)


if __name__ == "__main__":
    kgc = KGC()
    kgc.set_up()
    print(kgc.get_Ppub())

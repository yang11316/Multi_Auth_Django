from .utils import *
from typing import List, Tuple
import gmpy2


BITS = 256
class KGC:
    def __init__(self, bits: int = BITS) -> None:
        self.bits = bits
        self.acc_publickey: int = None
        # generater of accumulater
        self.G: int = None
        self.acc_cur: int = None
        self.kgc_Ppub:int = None
        self.kgc_q:int = None

    def update_witness(self,aux:str,witness:str)->str:
        new_witness:int = gmpy2.powmod(hex2int(witness),hex2int(aux),self.acc_publickey)
        return int2hex(new_witness)
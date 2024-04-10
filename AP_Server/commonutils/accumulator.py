from .utils import *
from typing import List, Tuple
import gmpy2


BITS = 256
class Accumulator:
    def __init__(self, bits: int = BITS) -> None:
        self.bits = bits
        self.N: int = hex2int("a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43")
        # generater of accumulater
        self.G: int = None
        self.acc_cur: int = None

    def update_witness(self,aux:str,witness:str)->str:
        new_witness:int = gmpy2.powmod(hex2int(witness),hex2int(aux),self.N)
        return int2hex(new_witness)
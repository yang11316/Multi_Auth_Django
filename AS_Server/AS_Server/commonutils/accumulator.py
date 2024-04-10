from .utils import *
import secrets
from typing import List, Tuple
import gmpy2
import time
import json


BITS = 256


class Accumulator:
    """RSA accumulator"""

    def __init__(self, bits: int = BITS) -> None:
        self.bits = bits
        self.pids: List[str] = []
        self.N: int = None
        self.serect_key: Tuple[int, int] = None
        # generater of accumulater
        self.G: int = None
        self.acc_cur: int = None

    def setup_from_file(self, file_path: str) -> None:
        with open(file_path, "r") as f:
            data = json.load(f)
            self.N = hex2int(data["N"])
            self.G = hex2int(data["G"])
            self.acc_cur = hex2int(data["acc_cur"])
            self.serect_key = (
                hex2int(data["serect_key_0"]),
                hex2int(data["serect_key_1"]),
            )

    def setup(self) -> None:
        """
        generate the accumulator
        """
        p = gmpy2.next_prime(secrets.randbits(self.bits))
        q = gmpy2.next_prime(secrets.randbits(self.bits))
        # make sure p and q are not the same
        while q == p:
            q = gmpy2.next_prime(secrets.randbits(self.bits))
        self.G = secrets.randbits(self.bits)
        self.acc_cur = self.G
        self.N = p * q
        self.serect_key = (p, q)

    def add_member(self, pid: str) -> None:
        """add member to accumulator"""
        self.pids.append(pid)
        self.acc_cur = gmpy2.powmod(self.acc_cur, hex2int(pid), self.N)
        """it need send aux to member"""
        """
        wait for update
        """

    def witness_generate_by_pid(self, pid: str) -> str:
        """generate witness by pid"""
        product: int = 1
        for tmp_pid in self.pids:
            if tmp_pid != pid:
                product *= hex2int(tmp_pid)
        witness: str = int2hex(gmpy2.powmod(self.G, product, self.N))
        return witness

    def witness_generate_all(self):
        """generate witness for all pids"""
        # 最初始时使用，后面使用by pid方法生成witness
        witness: List[str] = [self.witness_generate_by_pid(pid) for pid in self.pids]
        return self.pids, witness

    def verify_member(self, pid: str, witness: int) -> bool:
        """verify member"""
        res: int = gmpy2.powmod(hex2int(witness), hex2int(pid), self.N)
        return res == self.acc_cur

    def remove_member(self, pid: str) -> str:
        """remove member"""

        if pid not in self.pids:
            raise Exception("pid not in accumulator")
        euler_pk: int = (self.serect_key[0] - 1) * (self.serect_key[1] - 1)
        aux: int = gmpy2.invert(hex2int(pid), euler_pk)
        self.acc_cur = gmpy2.powmod(self.acc_cur, aux, self.N)

        self.pids.remove(pid)
        return int2hex(aux)

    def update_witness(self, aux: str, witness: str) -> str:
        new_witness: int = gmpy2.powmod(hex2int(witness), hex2int(aux), self.N)
        return int2hex(new_witness)

    def remove_member_list(self, pid_list: List[str]) -> str:
        """
        remove member from accumulator
        :param pid:list of pid
        :return:aux
        """
        isEffective: bool = True
        X: int = 1
        for pid in pid_list:
            if pid not in self.pids:
                isEffective = False
                break
            X *= hex2int(pid)
        if not isEffective:
            raise Exception("pid not in accumulator")
        euler_pk: int = (self.serect_key[0] - 1) * (self.serect_key[1] - 1)
        aux: int = gmpy2.invert(X, euler_pk)
        self.acc_cur = gmpy2.powmod(self.acc_cur, aux, self.N)
        for pid in pid_list:
            self.pids.remove(pid)
        return int2hex(aux)

    def save_accumlator_parameters(self, save_path: str = "./accumulator.json") -> None:
        """write accumulator parameter to json"""
        output: dict = {
            "N": int2hex(self.N),
            "G": int2hex(self.G),
            "acc_cur": int2hex(self.acc_cur),
            "serect_key_0": int2hex(self.serect_key[0]),
            "serect_key_1": int2hex(self.serect_key[1]),
        }

        with open(save_path, "w") as f:
            json.dump(output, f, indent=4)


if __name__ == "__main__":
    acc = Accumulator()
    acc.setup_from_file("./accumulator.json")
    print(int2hex(acc.acc_cur))

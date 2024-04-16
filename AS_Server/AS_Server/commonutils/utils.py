from cryptography.hazmat.primitives import hashes
from fastecdsa import point
from gmpy2 import next_prime
import secrets
import time


def calculate_pid(file_hash: str, pc_ip: str) -> str:
    """calculate pid"""
    tmp_hash = hashes.Hash(hashes.MD5())
    tmp_hash.update((file_hash + pc_ip).encode())
    # random
    tmp_hash.update(secrets.token_hex(16).encode())
    tmp_pid: str = tmp_hash.finalize().hex()
    pid: str = int2hex(next_prime(hex2int(tmp_pid)))
    return pid


def calculate_file_hash(file_path) -> str:
    """MD5 encoding file to hex string 32bytes"""
    with open(file_path, "rb") as f:
        file_hash = hashes.Hash(hashes.MD5())
        while chunk := f.read(4096):
            file_hash.update(chunk)
        return file_hash.finalize().hex()


def calculate_str_hash(std: str) -> str:
    tmp_hash = hashes.Hash(hashes.MD5())
    tmp_hash.update(std.encode())
    return tmp_hash.finalize().hex()


def hex2int(hex: str) -> int:
    """conver hex string to int"""
    return int(hex, 16)


def int2hex(num: int) -> str:
    """conver int to hex string"""
    return hex(num)[2:].tolower()


def get_bites(num: int, bits: int) -> str:
    """get bits of num"""
    return bin(num)[2:].zfill(bits)


def get_bits_length(num: int) -> int:
    """get bits length of num"""
    return len(get_bites(num, 128))


def point2hex(p: point.Point) -> str:
    """convert point to hex string"""
    return str(p.x) + str(p.y)


def get_time_stamp() -> str:
    """get the current time stamp"""
    return str(int(time.time()))


def get_time_point() -> float:
    """get time point"""
    return time.perf_counter()


def get_duration(start: float, end: float) -> float:
    """
    Calculate the duration between two time points in milliseconds.

    Parameters:
    start_time (float): The start time in seconds.
    end_time (float): The end time in seconds.

    Returns:
    float: The duration between start_time and end_time in seconds.
    """

    return end - start


if __name__ == "__main__":
    import os

    start = get_time_point()
    print(os.listdir())
    file_hash = calculate_file_hash("./manage.py")
    print(file_hash)
    print(hex2int(file_hash))
    print(int2hex(hex2int(file_hash)))
    print(get_bites(hex2int(file_hash), 64))
    print(get_bits_length(hex2int(file_hash)))
    print(get_duration(start, get_time_point()))
    print(secrets.token_hex(16))
    print(calculate_pid("bcd50201d588932dfc271f0489bbf823", "192.168.1.1"))

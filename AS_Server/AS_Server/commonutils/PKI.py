import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta


def generate_private_key():
    """生成RSA私钥。"""
    # 使用RSA算法生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # 公共指数，通常为65537
        key_size=2048,  # 密钥长度为2048位
        backend=default_backend(),  # 使用默认的后端
    )
    return private_key


def generate_self_signed_certificate(private_key, subject_name):
    """生成自签名证书。"""
    # 创建证书的主题
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, subject_name),  # 设置证书的通用名称
            x509.NameAttribute(
                NameOID.ORGANIZATION_NAME, "My Organization"
            ),  # 设置证书的组织名称
            x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),  # 设置证书的国家名称
            x509.NameAttribute(
                NameOID.STATE_OR_PROVINCE_NAME, "Beijing"
            ),  # 设置证书的省份名称
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Beijing"),  # 设置证书的城市名称
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, ""),  # 设置证书的邮箱地址
            x509.NameAttribute(
                NameOID.ORGANIZATION_NAME, "My Company"
            ),  # 设置证书的公司名称
        ]
    )
    now = datetime.utcnow()  # 获取当前UTC时间
    # 构建证书
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)  # 设置证书的主题
        .issuer_name(subject)  # 设置证书的颁发者，自签名证书颁发者和主题相同
        .public_key(private_key.public_key())  # 设置证书的公钥
        .serial_number(x509.random_serial_number())  # 生成随机序列号
        .not_valid_before(now)  # 设置证书的生效时间
        .not_valid_after(now + timedelta(days=365))  # 设置证书的过期时间，有效期为365天
        .sign(private_key, hashes.SHA256(), default_backend())
    )  # 使用私钥和SHA256算法签名证书
    return cert


def generate_certificate_signing_request(private_key, subject_name):
    """生成证书签名请求。"""
    # 创建证书请求的主题
    subject = x509.Name(
        [
            x509.NameAttribute(
                NameOID.COMMON_NAME, subject_name
            ),  # 设置证书请求的通用名称
            x509.NameAttribute(
                NameOID.ORGANIZATION_NAME, "My Organization"
            ),  # 设置证书的组织名称
            x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),  # 设置证书的国家名称
            x509.NameAttribute(
                NameOID.STATE_OR_PROVINCE_NAME, "Beijing"
            ),  # 设置证书的省份名称
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Beijing"),  # 设置证书的城市名称
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, ""),  # 设置证书的邮箱地址
            x509.NameAttribute(
                NameOID.ORGANIZATION_NAME, "My Company"
            ),  # 设置证书的公司名称
        ]
    )
    # 构建证书签名请求
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .sign(private_key, hashes.SHA256(), default_backend())
    )  # 使用私钥和SHA256算法签名证书请求
    return csr


def sign_certificate(csr, ca_cert, ca_private_key):
    """使用CA证书签署证书签名请求。"""
    now = datetime.utcnow()  # 获取当前UTC时间
    # 构建证书
    cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)  # 设置证书的主题，从CSR中获取
        .issuer_name(ca_cert.subject)  # 设置证书的颁发者，使用CA证书的主题
        .public_key(csr.public_key())  # 设置证书的公钥，从CSR中获取
        .serial_number(x509.random_serial_number())  # 生成随机序列号
        .not_valid_before(now)  # 设置证书的生效时间
        .not_valid_after(now + timedelta(days=365))  # 设置证书的过期时间，有效期为365天
        .sign(ca_private_key, hashes.SHA256(), default_backend())
    )  # 使用CA私钥和SHA256算法签名证书
    return cert


def verify_certificate(cert, ca_cert):
    """验证证书是否由CA证书签名。"""
    try:
        ca_public_key = ca_cert.public_key()  # 获取CA证书的公钥
        # 使用CA公钥验证证书的签名
        ca_public_key.verify(
            cert.signature,  # 证书的签名
            cert.tbs_certificate_bytes,  # 证书的TBS（To Be Signed）数据
            padding.PKCS1v15(),  # 使用PKCS1 v1.5填充
            cert.signature_hash_algorithm,  # 证书的签名哈希算法
        )
        return True  # 验证成功返回True
    except Exception:
        return False  # 验证失败返回False


def save_key_to_pem_file(key, filename):
    """将私钥保存到PEM文件中。"""
    # 将私钥转换为PEM格式
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,  # 使用PEM编码
        format=serialization.PrivateFormat.PKCS8,  # 使用PKCS8格式
        encryption_algorithm=serialization.NoEncryption(),  # 不使用加密
    )
    # 将PEM数据写入文件
    with open(filename, "wb") as f:
        f.write(pem)


def save_cert_to_pem_file(cert, filename):
    """将证书保存到PEM文件中。"""
    # 将证书转换为PEM格式
    pem = cert.public_bytes(encoding=serialization.Encoding.PEM)  # 使用PEM编码
    # 将PEM数据写入文件
    with open(filename, "wb") as f:
        f.write(pem)


def load_key_from_pem_file(filename):
    """从PEM文件中加载私钥。"""
    # 从文件中读取PEM数据
    with open(filename, "rb") as f:
        pem = f.read()
    # 从PEM数据中加载私钥
    private_key = serialization.load_pem_private_key(
        pem, password=None, backend=default_backend()
    )
    return private_key


def load_cert_from_pem_file(filename):
    """从PEM文件中加载证书。"""
    # 从文件中读取PEM数据
    with open(filename, "rb") as f:
        pem = f.read()
    # 从PEM数据中加载证书
    cert = x509.load_pem_x509_certificate(pem, default_backend())
    return cert


def load_cert_from_string(cert_string):
    """从字符串中加载证书。"""
    # 从字符串中加载证书
    cert = x509.load_pem_x509_certificate(cert_string.encode(), default_backend())
    return cert


def load_cert_as_string(cert):
    """将证书转换为字符串。"""
    # 将证书转换为PEM格式
    pem = cert.public_bytes(encoding=serialization.Encoding.PEM)  # 使用PEM编码
    return pem.decode()

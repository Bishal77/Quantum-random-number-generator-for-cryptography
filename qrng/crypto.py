# qrng/crypto.py
"""
Cryptographic operations using quantum-generated random keys.
Provides AES encryption/decryption and key generation from quantum bits.
"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import binascii
import hashlib
import hmac
from typing import Tuple, Optional


def bits_to_bytes(bitstr: str) -> bytes:
    """
    Convert a bitstring to bytes.
    
    If bitstring length is not a multiple of 8, pad with zeros on the right.
    
    Args:
        bitstr (str): Binary string (e.g., '11010110').
    
    Returns:
        bytes: Bytes representation of the bitstring.
    """
    # handle empty bitstring
    if not bitstr:
        return b""
    # pad bitstr to full bytes
    if len(bitstr) % 8 != 0:
        bitstr = bitstr.ljust(((len(bitstr) // 8) + 1) * 8, '0')
    b = int(bitstr, 2).to_bytes(len(bitstr) // 8, byteorder='big')
    return b


def bytes_to_hex(b: bytes) -> str:
    """
    Convert bytes to hexadecimal string representation.
    
    Args:
        b (bytes): Bytes to convert.
    
    Returns:
        str: Hexadecimal string.
    """
    return binascii.hexlify(b).decode()


def generate_aes_key_from_bits(bitstr: str, key_size_bits: int = 256) -> bytes:
    """
    Create AES key bytes (128/192/256) from a bitstring.
    
    Args:
        bitstr (str): Binary string of quantum-generated bits.
        key_size_bits (int): Desired key size in bits (128, 192, or 256).
    
    Returns:
        bytes: AES key of specified size.
    
    Raises:
        ValueError: If bitstr is shorter than key_size_bits.
    """
    if len(bitstr) < key_size_bits:
        raise ValueError("bitstr shorter than requested key size")
    key_bits = bitstr[:key_size_bits]
    return bits_to_bytes(key_bits)


def generate_aes_key_from_bits_kdf(bitstr: str, key_size_bits: int = 256, salt: Optional[bytes] = None) -> Tuple[bytes, str]:
    """
    Derive an AES key from a (possibly longer) bitstring using HKDF-SHA256.

    This is a safer, non-predictable production-friendly method. It uses
    the bitstring as input keying material (IKM), generates a random salt
    if none is provided, and runs HKDF-Extract/Expand to produce the
    desired key length.

    Args:
        bitstr (str): Binary string of quantum-generated bits.
        key_size_bits (int): Desired key size in bits (128, 192, or 256).
        salt (bytes|None): Optional salt to use; if None a new random salt is generated.

    Returns:
        (key_bytes, salt_hex): tuple containing the derived key bytes and the salt as hex string.
    """
    if key_size_bits not in (128, 192, 256):
        raise ValueError("key_size_bits must be one of 128, 192, or 256")
    # Convert bitstring to bytes (IKM). If empty, error.
    ikm = bits_to_bytes(bitstr)
    if not ikm:
        raise ValueError("bitstr must contain some bits for KDF")

    if salt is None:
        salt = get_random_bytes(16)

    # HKDF-Extract: PRK = HMAC-Hash(salt, IKM)
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()

    # HKDF-Expand: generate enough blocks
    hash_len = hashlib.sha256().digest_size
    n_blocks = (key_size_bits // 8 + hash_len - 1) // hash_len
    okm = b''
    previous = b''
    info = b'qrng-aes-key-derivation'
    for i in range(1, n_blocks + 1):
        previous = hmac.new(prk, previous + info + bytes([i]), hashlib.sha256).digest()
        okm += previous

    key_bytes = okm[: key_size_bits // 8]
    return key_bytes, binascii.hexlify(salt).decode()


from typing import Union


def aes_encrypt(key: bytes, plaintext: Union[bytes, str]) -> dict:
    """
    AES-CBC encrypt with random IV.
    
    Args:
        key (bytes): AES key (128, 192, or 256 bits).
        plaintext (bytes): Data to encrypt.
    
    Returns:
        dict: Dictionary with 'iv' and 'ciphertext' in hexadecimal format.
    """
    # accept str or bytes for plaintext
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(plaintext, AES.block_size))
    return {'iv': bytes_to_hex(iv), 'ciphertext': bytes_to_hex(ct)}


def aes_decrypt(key: bytes, iv_hex: str, ciphertext_hex: str) -> bytes:
    """
    AES-CBC decrypt using provided IV.
    
    Args:
        key (bytes): AES key (must match encryption key).
        iv_hex (str): Initialization vector in hexadecimal format.
        ciphertext_hex (str): Ciphertext in hexadecimal format.
    
    Returns:
        bytes: Decrypted plaintext.
    """
    iv = binascii.unhexlify(iv_hex)
    ct = binascii.unhexlify(ciphertext_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

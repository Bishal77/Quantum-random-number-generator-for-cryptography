"""
Unit tests for qrng.crypto module
Tests AES encryption, decryption, and key generation
"""
import pytest
from qrng.crypto import (
    bits_to_bytes,
    bytes_to_hex,
    generate_aes_key_from_bits,
    aes_encrypt,
    aes_decrypt
)


class TestBitsToBytes:
    """Test suite for bits_to_bytes function"""

    def test_byte_aligned_bits(self):
        """Test with byte-aligned bitstring"""
        result = bits_to_bytes('11111111')
        assert result == b'\xff'
        assert len(result) == 1

    def test_multiple_bytes(self):
        """Test with multiple bytes"""
        result = bits_to_bytes('1111111100000000')
        assert result == b'\xff\x00'
        assert len(result) == 2

    def test_zero_byte(self):
        """Test zero byte"""
        result = bits_to_bytes('00000000')
        assert result == b'\x00'

    def test_padding_with_zeros(self):
        """Test that non-byte-aligned bits are padded"""
        result = bits_to_bytes('1')  # Single bit
        assert len(result) == 1
        assert result == b'\x80'  # 10000000 in binary

    def test_empty_string(self):
        """Test empty bitstring"""
        result = bits_to_bytes('')
        assert result == b''


class TestBytesToHex:
    """Test suite for bytes_to_hex function"""

    def test_basic_conversion(self):
        """Test basic bytes to hex"""
        result = bytes_to_hex(b'\xff')
        assert result == 'ff'

    def test_multiple_bytes(self):
        """Test multiple bytes to hex"""
        result = bytes_to_hex(b'\xff\x00\xaa')
        assert result == 'ff00aa'

    def test_zero_bytes(self):
        """Test zero bytes"""
        result = bytes_to_hex(b'\x00')
        assert result == '00'

    def test_empty_bytes(self):
        """Test empty bytes"""
        result = bytes_to_hex(b'')
        assert result == ''


class TestGenerateAESKeyFromBits:
    """Test suite for generate_aes_key_from_bits function"""

    def test_256_bit_key(self):
        """Test 256-bit key generation"""
        bitstring = '1' * 256
        key = generate_aes_key_from_bits(bitstring, key_size_bits=256)
        assert len(key) == 32  # 256 bits / 8

    def test_192_bit_key(self):
        """Test 192-bit key generation"""
        bitstring = '1' * 192
        key = generate_aes_key_from_bits(bitstring, key_size_bits=192)
        assert len(key) == 24  # 192 bits / 8

    def test_128_bit_key(self):
        """Test 128-bit key generation"""
        bitstring = '1' * 128
        key = generate_aes_key_from_bits(bitstring, key_size_bits=128)
        assert len(key) == 16  # 128 bits / 8

    def test_key_from_longer_bitstring(self):
        """Test key extraction from longer bitstring"""
        bitstring = '1' * 512
        key = generate_aes_key_from_bits(bitstring, key_size_bits=256)
        assert len(key) == 32
        # Should use first 256 bits

    def test_insufficient_bits(self):
        """Test error on insufficient bits"""
        bitstring = '1' * 128
        with pytest.raises(ValueError):
            generate_aes_key_from_bits(bitstring, key_size_bits=256)

    def test_key_randomness(self):
        """Test that different bitstrings produce different keys"""
        key1 = generate_aes_key_from_bits('0' * 256, key_size_bits=256)
        key2 = generate_aes_key_from_bits('1' * 256, key_size_bits=256)
        assert key1 != key2


class TestAESEncryptDecrypt:
    """Test suite for AES encryption and decryption"""

    def test_encrypt_decrypt_roundtrip(self):
        """Test encryption and decryption"""
        key = b'\x00' * 32  # 256-bit key
        plaintext = b"Hello, World!"
        
        encrypted = aes_encrypt(key, plaintext)
        assert 'iv' in encrypted
        assert 'ciphertext' in encrypted
        
        decrypted = aes_decrypt(key, encrypted['iv'], encrypted['ciphertext'])
        assert decrypted == plaintext

    def test_different_message_lengths(self):
        """Test encryption with various message lengths"""
        key = b'\x00' * 32
        messages = [
            b"A",
            b"Hello",
            b"The quick brown fox jumps over the lazy dog",
            b"x" * 1000
        ]
        
        for msg in messages:
            encrypted = aes_encrypt(key, msg)
            decrypted = aes_decrypt(key, encrypted['iv'], encrypted['ciphertext'])
            assert decrypted == msg

    def test_different_encryption_produces_different_ciphertext(self):
        """Test that same plaintext produces different ciphertext due to random IV"""
        key = b'\x00' * 32
        plaintext = b"Same plaintext"
        
        enc1 = aes_encrypt(key, plaintext)
        enc2 = aes_encrypt(key, plaintext)
        
        # Different IVs should produce different ciphertexts
        assert enc1['iv'] != enc2['iv']
        assert enc1['ciphertext'] != enc2['ciphertext']
        
        # But both should decrypt to original
        assert aes_decrypt(key, enc1['iv'], enc1['ciphertext']) == plaintext
        assert aes_decrypt(key, enc2['iv'], enc2['ciphertext']) == plaintext

    def test_wrong_key_decryption_fails(self):
        """Test that wrong key cannot decrypt"""
        key1 = b'\x00' * 32
        key2 = b'\xff' * 32
        plaintext = b"Secret message"
        
        encrypted = aes_encrypt(key1, plaintext)
        
        with pytest.raises(ValueError):
            # Should fail due to padding validation
            aes_decrypt(key2, encrypted['iv'], encrypted['ciphertext'])

    def test_hex_format_output(self):
        """Test that IV and ciphertext are hex format"""
        key = b'\x00' * 32
        plaintext = b"Test"
        
        encrypted = aes_encrypt(key, plaintext)
        
        # Check hex format
        assert all(c in '0123456789abcdef' for c in encrypted['iv'])
        assert all(c in '0123456789abcdef' for c in encrypted['ciphertext'])
        
        # IV should be 32 chars (16 bytes in hex)
        assert len(encrypted['iv']) == 32


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

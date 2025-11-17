from flask import Flask, render_template, request, jsonify
from qrng.runner import generate_random_bits
from qrng.crypto import generate_aes_key_from_bits, aes_encrypt, aes_decrypt

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_demo():
    data = request.json or {}
    # Read parameters with safe defaults
    key_bits = int(data.get("key_bits", 128))
    n_qubits = int(data.get("n_qubits", 4))
    shots = int(data.get("shots", 1))
    unbiased = bool(data.get("unbiased", True))
    message = data.get("message", "hello")

    # Generate bits and derive key
    bits = generate_random_bits(target_bits=key_bits, n_qubits=n_qubits, shots_per_call=shots, unbiased=unbiased)
    try:
        key = generate_aes_key_from_bits(bits)
        kdf_salt = None
    except Exception:
        # If bitstring is too short for direct truncation, fall back to HKDF-style KDF
        try:
            from qrng.crypto import generate_aes_key_from_bits_kdf

            key, kdf_salt = generate_aes_key_from_bits_kdf(bits)
        except Exception:
            # As a last resort, derive a key from available bits by padding/truncating bytes
            from hashlib import sha256

            key = sha256(bits.encode() if isinstance(bits, str) else bits).digest()[:16]
            kdf_salt = None

    # Encrypt / decrypt
    enc = aes_encrypt(key, message.encode())
    # enc returns hex strings for iv/ciphertext in this project API
    iv_raw = enc.get("iv")
    ct_raw = enc.get("ciphertext")
    # ensure we have hex strings
    if isinstance(iv_raw, str):
        iv_hex = iv_raw
    else:
        iv_hex = iv_raw.hex()
    if isinstance(ct_raw, str):
        ct_hex = ct_raw
    else:
        ct_hex = ct_raw.hex()

    decrypted = aes_decrypt(key, iv_hex, ct_hex)
    decrypted_text = decrypted.decode(errors="replace")

    result = {
        "key_hex": key.hex(),
        "kdf_salt": kdf_salt,
        "iv_hex": iv_hex,
        "ciphertext_hex": ct_hex,
        "decrypted": decrypted_text,
        "bits_len": len(bits),
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

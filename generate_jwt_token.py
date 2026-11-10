python3 -c '
import base64, hmac, hashlib, json

header = json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
payload = json.dumps({"sub": "test_admin"}).encode()

def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

h_enc = b64url(header)
p_enc = b64url(payload)
msg = f"{h_enc}.{p_enc}".encode()

secret = b"super-secret-key-for-training-must-be-32-bytes-long!!"
sig = hmac.new(secret, msg, hashlib.sha256).digest()
print(f"{h_enc}.{p_enc}.{b64url(sig)}")
'

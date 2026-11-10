TOKEN=$(python3 -c '
import base64, hmac, hashlib, json
h = base64.urlsafe_b64encode(json.dumps({"alg":"HS256","typ":"JWT"}).encode()).rstrip(b"=").decode()
p = base64.urlsafe_b64encode(json.dumps({"sub":"test_admin"}).encode()).rstrip(b"=").decode()
sig = base64.urlsafe_b64encode(hmac.new(b"super-secret-key-for-training-must-be-32-bytes-long!!", f"{h}.{p}".encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
print(f"{h}.{p}.{sig}")
')

curl -i -H "Authorization: Bearer $TOKEN" http://localhost:8001/employees

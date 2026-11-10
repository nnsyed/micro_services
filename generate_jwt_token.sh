#!/bin/bash

# Your secret key matching your application config
SECRET="super-secret-key-for-training-must-be-32-bytes-long!!"

# Base64 URL-encode helper function
base64url() {
    openssl base64 -e -A | tr '+/' '-_' | tr -d '='
}

# 1. Header & Payload
HEADER='{"alg":"HS256","typ":"JWT"}'
PAYLOAD='{"sub":"test_admin"}'

# 2. Encode Header and Payload
B64_HEADER=$(echo -n "$HEADER" | base64url)
B64_PAYLOAD=$(echo -n "$PAYLOAD" | base64url)

# 3. Create HMAC-SHA256 Signature
SIGNATURE=$(echo -n "$B64_HEADER.$B64_PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" -binary | base64url)

# 4. Output the complete JWT token
echo "Generated JWT Token:"
echo "$B64_HEADER.$B64_PAYLOAD.$SIGNATURE"

from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
import jwt
import os

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "super-secret-key-for-training"
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try: return jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError: raise HTTPException(status_code=401, detail="Invalid token")

r = redis.Redis(host=os.getenv("REDIS_HOST", "redis-db"), port=6379, decode_responses=True)

# 1. READ ALL KEYS & VALUES
@app.get("/cache")
def read_all_cache(user: dict = Depends(verify_token)):
    keys = r.keys("*")
    cache_dump = {k: r.get(k) for k in keys}
    return {"data": cache_dump}

# 2. WRITE / UPDATE
@app.post("/cache")
def set_cache(payload: dict = Body(...), user: dict = Depends(verify_token)):
    r.set(payload["key"], payload["value"])
    return {"status": "success"}

# 3. DELETE
@app.delete("/cache/{key}")
def delete_cache(key: str, user: dict = Depends(verify_token)):
    r.delete(key)
    return {"status": "evicted"}
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import jwt
import os

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "super-secret-key-for-training"
ALGORITHM = "HS256"

class EmployeeSchema(BaseModel):
    name: str
    role: str
    department: str

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token verification metadata")

def get_db():
    return psycopg2.connect(host=os.getenv("DB_HOST", "sql-db"), database="company", user="postgres", password="postgres_password")

# 1. READ ALL
@app.get("/employees")
def read_all(user: dict = Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, name, role, department FROM employees ORDER BY id ASC;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"data": data}

# 2. CREATE
@app.post("/employees")
def create_emp(emp: EmployeeSchema, user: dict = Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, role, department) VALUES (%s, %s, %s);", (emp.name, emp.role, emp.department))
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "created"}

# 3. UPDATE
@app.put("/employees/{emp_id}")
def update_emp(emp_id: int, emp: EmployeeSchema, user: dict = Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET name=%s, role=%s, department=%s WHERE id=%s;", (emp.name, emp.role, emp.department, emp_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "updated"}

# 4. DELETE
@app.delete("/employees/{emp_id}")
def delete_emp(emp_id: int, user: dict = Depends(verify_token)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s;", (emp_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "deleted"}
FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn psycopg2-binary PyJWT
COPY main.py .
EXPOSE 8001
# FIX: Removed the ".py" extension from the module path
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
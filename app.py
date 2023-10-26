import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_PRODUCT_TABLE = (
    "CREATE TABLE IF NOT EXISTS product(id SERIAL PRIMARY KEY, name TEXT);"
)

INSERT_PRODUCT_RETURN_ID = "INSERT INTO product(name) VALUES (%s) RETURNING id;"

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.get("/")
def home():
    return "Hello, world!"
@app.post("/api/room")
def create_room():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PRODUCT_TABLE)
            cursor.execute(INSERT_PRODUCT_RETURN_ID, (name,))
            product_id = cursor.fetchone()[0]
    return {"id": product_id, "message": f"Product {name} created."}, 201



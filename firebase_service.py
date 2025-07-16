import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_product(user_id, data):
    db.collection("users").document(user_id).collection("products").add(data)

def get_inventory_alerts(user_id):
    products_ref = db.collection("users").document(user_id).collection("products")
    alerts = []
    for product in products_ref.stream():
        prod = product.to_dict()
        if int(prod.get("quantity", 0)) < 5:
            alerts.append({"name": prod.get("name"), "quantity": prod.get("quantity")})
    return alerts

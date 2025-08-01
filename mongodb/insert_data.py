from pymongo import MongoClient
import json

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")

# Veritabanı ve koleksiyonlar
db = client["hotel_data"]
customers_collection = db["customers"]
reservations_collection = db["reservations"]

# Önceki verileri temizle (opsiyonel)
customers_collection.delete_many({})
reservations_collection.delete_many({})

# JSON dosyalarını oku
with open("data/sample_customers.json") as f:
    customers = json.load(f)

with open("data/sample_reservations.json") as f:
    reservations = json.load(f)

# MongoDB'ye ekle
customers_collection.insert_many(customers)
reservations_collection.insert_many(reservations)

print("Otel verileri MongoDB'ye yüklendi.")

from pymongo import MongoClient
import pandas as pd

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["hotel_data"]
customers_col = db["customers"]
reservations_col = db["reservations"]


customers = list(customers_col.find())
reservations = list(reservations_col.find())

customers_df = pd.DataFrame(customers)
reservations_df = pd.DataFrame(reservations)


reservations_df["check_in"] = pd.to_datetime(reservations_df["check_in"])
reservations_df["check_out"] = pd.to_datetime(reservations_df["check_out"])

reservations_df["stay_length"] = (reservations_df["check_out"] - reservations_df["check_in"]).dt.days

merged_df = pd.merge(reservations_df, customers_df, on="customer_id", how="left")


avg_stay = reservations_df["stay_length"].mean()
print("Ortalama konaklama süresi (gün):", round(avg_stay, 2))

total_spent_per_customer = merged_df.groupby("name")["price"].sum().sort_values(ascending=False)
print("\nMüşteri bazında toplam harcama:\n", total_spent_per_customer)

top_customers = merged_df["name"].value_counts().head(3)
print("\nEn çok rezervasyon yapan müşteriler:\n", top_customers)

cancel_rate = (reservations_df["status"] == "Cancelled").mean()
print("\nİptal edilen rezervasyon oranı: %", round(cancel_rate * 100, 2))

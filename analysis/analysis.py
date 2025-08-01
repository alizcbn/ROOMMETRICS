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


import matplotlib.pyplot as plt
import seaborn as sns

# 1. İptal edilmeyen rezervasyonlara göre toplam harcama
completed_reservations = merged_df[merged_df["status"] == "Completed"]
total_spent_completed = completed_reservations.groupby("name")["price"].sum().sort_values(ascending=False)
print("\nİptal edilmeyen rezervasyonlara göre toplam harcama:\n", total_spent_completed)

# 2. Ülke bazında müşteri sayısı ve toplam gelir
customers_per_country = customers_df["country"].value_counts()
print("\nÜlke bazında müşteri sayısı:\n", customers_per_country)

revenue_per_country = completed_reservations.groupby("country")["price"].sum().sort_values(ascending=False)
print("\nÜlke bazında toplam gelir:\n", revenue_per_country)

# 3. Oda tipine göre ortalama fiyat ve rezervasyon sayısı
avg_price_per_room = completed_reservations.groupby("room_type")["price"].mean()
count_per_room = completed_reservations["room_type"].value_counts()
print("\nOda tipine göre ortalama fiyat:\n", avg_price_per_room)
print("\nOda tipine göre rezervasyon sayısı:\n", count_per_room)

# 4. Müşteri yaş gruplarına göre analiz
bins = [0, 30, 40, 50, 100]
labels = ["<30", "31-40", "41-50", "50+"]

customers_df["age_group"] = pd.cut(customers_df["age"], bins=bins, labels=labels, right=False)

age_group_counts = customers_df["age_group"].value_counts().sort_index()
print("\nYaş grubuna göre müşteri sayısı:\n", age_group_counts)

merged_completed = pd.merge(completed_reservations, customers_df, on="customer_id", how="left")
spend_per_age_group = merged_completed.groupby("age_group")["price"].sum()
print("\nYaş grubuna göre toplam harcama:\n", spend_per_age_group)

# --- GÖRSELLEŞTİRMELER ---

sns.set(style="whitegrid")

plt.figure(figsize=(12, 8))

# Grafik 1: Ülke bazında müşteri sayısı
plt.subplot(2, 2, 1)
sns.barplot(x=customers_per_country.index, y=customers_per_country.values, palette="viridis")
plt.title("Country-wise Customer Count")
plt.xlabel("Country")
plt.ylabel("Number of Customers")

# Grafik 2: Ülke bazında toplam gelir
plt.subplot(2, 2, 2)
sns.barplot(x=revenue_per_country.index, y=revenue_per_country.values, palette="magma")
plt.title("Country-wise Total Revenue")
plt.xlabel("Country")
plt.ylabel("Revenue")

# Grafik 3: Oda tipine göre ortalama fiyat
plt.subplot(2, 2, 3)
sns.barplot(x=avg_price_per_room.index, y=avg_price_per_room.values, palette="coolwarm")
plt.title("Average Price per Room Type")
plt.xlabel("Room Type")
plt.ylabel("Average Price")

# Grafik 4: Müşteri yaş gruplarına göre toplam harcama
plt.subplot(2, 2, 4)
sns.barplot(x=spend_per_age_group.index.astype(str), y=spend_per_age_group.values, palette="pastel")
plt.title("Total Spending by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Total Spending")


plt.tight_layout()
plt.savefig("../docs/analysis_charts.png", dpi=300)
plt.show()


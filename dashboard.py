import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Dashboard Analisis Data E-Commerce")

# --- Load Data dari URL Google Drive ---
@st.cache_data
def load_data():
    orders = pd.read_csv("https://drive.google.com/uc?id=1LnrXg37tjuEA8tG_FFlvFuHipSw0lRXX")
    payments = pd.read_csv("https://drive.google.com/uc?id=1gRwmApgnQo8FgD61AsZc1pUTY7CYzblN")
    order_items = pd.read_csv("https://drive.google.com/uc?id=12ksgLbIxVr4-xmqPgWqOuhPoo-q7DeX7")
    products = pd.read_csv("https://drive.google.com/uc?id=1ARnbIOAiKsdTUKLlwO4zvmlIuqHRNPUL")
    rfm_table = pd.read_csv("https://drive.google.com/uc?id=1ysfBSYYZPaGpksnrDrVxEpVUbo7-Ak1e") 
    return orders, payments, order_items, products, rfm_table

orders, payments, order_items, products, rfm_table = load_data()

# Pastikan tipe data datetime
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

# Menambahkan fitur interaktif: Filter berdasarkan rentang tanggal
st.sidebar.subheader("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", orders["order_purchase_timestamp"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", orders["order_purchase_timestamp"].max())

# Filter dataset berdasarkan rentang tanggal
filtered_orders = orders[(orders["order_purchase_timestamp"] >= pd.Timestamp(start_date)) & 
                         (orders["order_purchase_timestamp"] <= pd.Timestamp(end_date))]

st.subheader(f"Ringkasan Data Pesanan dari {start_date} hingga {end_date}")
st.write(filtered_orders.describe())

# Menampilkan metrik utama
st.subheader("Metrik Utama")
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Pesanan", filtered_orders.shape[0])
col2.metric("Jumlah Produk", products.shape[0])
col3.metric("Jumlah Metode Pembayaran", payments['payment_type'].nunique())

# Visualisasi Tren Pesanan Berdasarkan Waktu
st.subheader("Tren Jumlah Pesanan Per Bulan")

filtered_orders["order_month"] = filtered_orders["order_purchase_timestamp"].dt.to_period("M")
monthly_orders = filtered_orders.groupby("order_month").size()

fig, ax = plt.subplots(figsize=(12, 5))
monthly_orders.plot(kind="line", marker="o", color="b", linestyle="dashed", ax=ax)
ax.set_title("Tren Jumlah Pesanan Per Bulan (Berdasarkan Filter)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# --- Visualisasi Distribusi RFM ---
st.subheader("Distribusi Recency, Frequency, dan Monetary")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(rfm_table["Recency"], bins=50, kde=True, color="blue", ax=axes[0])
axes[0].set_title("Distribusi Recency")

sns.histplot(rfm_table["Frequency"], bins=50, kde=True, color="green", ax=axes[1])
axes[1].set_title("Distribusi Frequency")

sns.histplot(rfm_table["Monetary"], bins=50, kde=True, color="red", ax=axes[2])
axes[2].set_title("Distribusi Monetary")

st.pyplot(fig)

# Menampilkan Insight
st.subheader("Insight dari Analisis RFM")
st.markdown("""
- **Recency**: Sebagian besar pelanggan terakhir melakukan transaksi dalam rentang waktu 50–300 hari yang lalu. Namun, ada kelompok pelanggan yang sudah lama tidak melakukan pembelian, bahkan lebih dari 600 hari. Strategi seperti retargeting melalui email atau penawaran eksklusif bisa diterapkan.
- **Frequency**: Mayoritas pelanggan hanya melakukan pembelian sekali atau dua kali, dengan sedikit pelanggan yang melakukan pembelian lebih dari lima kali. Program loyalitas dapat meningkatkan frekuensi pembelian.
- **Monetary**: Sebagian besar pelanggan memiliki total nilai transaksi di bawah 2.000, dengan hanya sedikit yang memiliki nilai transaksi tinggi. Strategi upselling dan bundling produk bisa diterapkan.
""")

# --- Pola Pembelian Berdasarkan Kategori Produk ---
st.subheader("Pola Pembelian Berdasarkan Kategori Produk")

@st.cache_data
def load_purchase_data():
    merged_data = order_items.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
    return merged_data['product_category_name'].value_counts()

category_counts = load_purchase_data()

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(x=category_counts.index[:15], y=category_counts.values[:15], palette="viridis", ax=ax)
ax.set_title("Kategori Produk Terlaris")
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Jumlah Pembelian")
plt.xticks(rotation=45)
st.pyplot(fig)

# --- Metode Pembayaran yang Paling Sering Digunakan ---
st.subheader("Metode Pembayaran yang Paling Sering Digunakan")

@st.cache_data
def load_payment_data():
    return payments['payment_type'].value_counts()

payment_trends = load_payment_data()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=payment_trends.index, y=payment_trends.values, palette="coolwarm", ax=ax)
ax.set_title("Distribusi Metode Pembayaran")
ax.set_xlabel("Metode Pembayaran")
ax.set_ylabel("Jumlah Transaksi")
st.pyplot(fig)

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("""
1. Kategori produk terlaris adalah Cama Mesa Banho, menunjukkan bahwa produk dalam kategori ini memiliki permintaan tinggi. Perusahaan bisa mempertimbangkan penambahan stok, diskon khusus, atau strategi bundling untuk meningkatkan penjualan lebih lanjut.


2. Metode pembayaran paling populer adalah Credit Card, yang menunjukkan preferensi pelanggan terhadap transaksi non-tunai. Promo seperti cicilan 0% atau cashback dapat digunakan untuk mendorong lebih banyak transaksi.


3. Analisis RFM memberikan wawasan tentang perilaku pelanggan:

- Recency: Sebagian besar pelanggan terakhir melakukan transaksi dalam rentang waktu 50–300 hari yang lalu. Namun, ada kelompok pelanggan yang sudah lama tidak melakukan pembelian, bahkan lebih dari 600 hari. Untuk mengaktifkan kembali pelanggan lama, strategi seperti retargeting melalui email, penawaran diskon eksklusif, atau kampanye re-engagement dapat diterapkan.

- Frequency: Mayoritas pelanggan hanya melakukan pembelian sekali atau dua kali, sedangkan pelanggan yang berbelanja lebih dari lima kali jumlahnya sangat sedikit. Hal ini menunjukkan perlunya program loyalitas, insentif untuk pembelian berulang, atau rekomendasi produk berbasis histori transaksi agar pelanggan lebih sering berbelanja.

- Monetary: Sebagian besar pelanggan memiliki total nilai transaksi di bawah 2.000, dengan hanya sedikit pelanggan yang memiliki total belanja tinggi. Untuk meningkatkan nilai transaksi, strategi seperti bundling produk, upselling, atau diskon khusus bagi pelanggan dengan pembelian di atas ambang tertentu bisa diterapkan.
""") 

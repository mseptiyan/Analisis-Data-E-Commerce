import streamlit as st
import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Judul Dashboard
st.title("Dashboard Analisis Data E-Commerce")

# --- Mengunduh Dataset dari Kaggle ---
@st.cache_data
def download_dataset():
    path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    return path

dataset_path = download_dataset()

# --- 2️⃣ Load Data ---
@st.cache_data
def load_data():
    orders = pd.read_csv(os.path.join(dataset_path, "olist_orders_dataset.csv"))
    payments = pd.read_csv(os.path.join(dataset_path, "olist_order_payments_dataset.csv"))
    order_items = pd.read_csv(os.path.join(dataset_path, "olist_order_items_dataset.csv"))
    products = pd.read_csv(os.path.join(dataset_path, "olist_products_dataset.csv"))
    rfm_table = pd.read_csv("https://drive.google.com/uc?id=1xAw1nw1KHC9PH7M83pskkNyYanBlWE-8") 
    return orders, payments, order_items, products

orders, payments, order_items, products, rfm_table = load_data()


# Menampilkan ringkasan data
st.subheader("Ringkasan Data RFM")
st.write(rfm_table.describe())

# Menampilkan metrik utama
st.subheader("Metrik Utama")
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Pesanan", orders.shape[0])
col2.metric("Jumlah Produk", products.shape[0])
col3.metric("Jumlah Metode Pembayaran", payments['payment_type'].nunique())

# Visualisasi Distribusi RFM
st.subheader("Distribusi Recency, Frequency, dan Monetary")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Recency
sns.histplot(rfm_table["Recency"], bins=50, kde=True, color="blue", ax=axes[0])
axes[0].set_title("Distribusi Recency")

# Frequency
sns.histplot(rfm_table["Frequency"], bins=50, kde=True, color="green", ax=axes[1])
axes[1].set_title("Distribusi Frequency")

# Monetary
sns.histplot(rfm_table["Monetary"], bins=50, kde=True, color="red", ax=axes[2])
axes[2].set_title("Distribusi Monetary")

st.pyplot(fig)

# Menampilkan Insight
st.subheader("Insight dari Analisis RFM")
st.markdown("""
- Recency: Sebagian besar pelanggan terakhir bertransaksi dalam 100-400 hari, tapi ada yang tidak belanja hingga 700 hari. Bisa diberikan diskon reaktivasi untuk menarik pelanggan lama.
- Frequency: Mayoritas pelanggan hanya belanja 1-2 kali, sehingga program loyalitas bisa menjadi solusi untuk meningkatkan retensi pelanggan.
- Monetary: Sebagian besar pelanggan memiliki total belanja di bawah 2000, jadi strategi upselling dan bundling bisa diterapkan untuk meningkatkan nilai transaksi.
""")

# --- Tambahan: Pola Pembelian Berdasarkan Kategori Produk ---
st.subheader("Pola Pembelian Berdasarkan Kategori Produk")

@st.cache_data
def load_purchase_data():
    merged_data = order_items.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
    return merged_data['product_category_name'].value_counts()

category_counts = load_purchase_data()

# Plot Pola Pembelian
fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(x=category_counts.index[:10], y=category_counts.values[:10], palette="viridis", ax=ax)
ax.set_title("Kategori Produk Terlaris")
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Jumlah Pembelian")
plt.xticks(rotation=45)
st.pyplot(fig)

# --- Tambahan: Metode Pembayaran yang Paling Sering Digunakan ---
st.subheader("Metode Pembayaran yang Paling Sering Digunakan")

@st.cache_data
def load_payment_data():
    return payments['payment_type'].value_counts()

payment_trends = load_payment_data()

# Plot Tren Pembayaran
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=payment_trends.index, y=payment_trends.values, palette="coolwarm", ax=ax)
ax.set_title("Distribusi Metode Pembayaran")
ax.set_xlabel("Metode Pembayaran")
ax.set_ylabel("Jumlah Transaksi")
st.pyplot(fig)

# Menampilkan Kesimpulan Akhir
st.subheader("Kesimpulan")
st.markdown("""
1. Kategori produk terlaris adalah Cama Mesa Banho, menunjukkan bahwa produk dalam kategori ini memiliki permintaan tinggi. Perusahaan bisa mempertimbangkan penambahan stok, diskon khusus, atau strategi bundling.
2. Metode pembayaran paling populer adalah Credit Card, menandakan bahwa pelanggan lebih nyaman bertransaksi dengan kartu kredit. Promo cicilan 0% atau cashback bisa menjadi strategi untuk menarik lebih banyak transaksi.

3. Analisis RFM menunjukkan bahwa banyak pelanggan hanya belanja sekali atau dua kali, sehingga strategi retargeting, program loyalitas, dan bundling dapat diterapkan untuk meningkatkan frekuensi transaksi.
""")

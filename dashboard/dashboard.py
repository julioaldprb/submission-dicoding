import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


# Mengatur style matplotlib
plt.style.use('seaborn-v0_8-darkgrid')



st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Fungsi untuk memuat data (menggunakan cache agar tidak di-load ulang setiap interaksi)
@st.cache
def load_data():
    hour_df = pd.read_csv("./data/hour.csv")
    day_df = pd.read_csv("./data/day.csv")
    # Konversi kolom 'dteday' menjadi datetime
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    # Mapping label musim
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    hour_df['season_label'] = hour_df['season'].map(season_labels)
    return hour_df, day_df

hour_df, day_df = load_data()

st.title("Dashboard Analisis Data Bike Sharing")
st.markdown("""
Dashboard ini bertujuan untuk mengeksplorasi **pengaruh cuaca** dan **musim** terhadap jumlah peminjaman sepeda.
""")

# Sidebar interaktif untuk filter data
st.sidebar.header("Filter Data")
selected_weathers = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca (weathersit)",
    options=sorted(hour_df['weathersit'].unique()),
    default=sorted(hour_df['weathersit'].unique())
)
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim",
    options=sorted(hour_df['season_label'].unique()),
    default=sorted(hour_df['season_label'].unique())
)

# Filter data berdasarkan pilihan di sidebar
filtered_df = hour_df[(hour_df['weathersit'].isin(selected_weathers)) & 
                      (hour_df['season_label'].isin(selected_seasons))]

st.write("Menampilkan data untuk kondisi cuaca:", selected_weathers, "dan musim:", selected_seasons)
st.dataframe(filtered_df.head())

# ========================
# Section 1: Pengaruh Cuaca
# ========================
st.header("Pertanyaan 1: Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda")

# 1. Boxplot: Distribusi jumlah peminjaman berdasarkan kondisi cuaca
fig1, ax1 = plt.subplots(figsize=(8,6))
sns.boxplot(x='weathersit', y='cnt', data=filtered_df, ax=ax1)
ax1.set_title("Boxplot: Jumlah Peminjaman Berdasarkan Kondisi Cuaca")
ax1.set_xlabel("Kondisi Cuaca (1: Clear, 2: Mist, 3: Light Rain/Snow, 4: Heavy Rain/Snow)")
ax1.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig1)

# 2. Barplot: Rata-rata peminjaman per kondisi cuaca
fig2, ax2 = plt.subplots(figsize=(8,6))
sns.barplot(x='weathersit', y='cnt', data=filtered_df, estimator=np.mean, ci=None, ax=ax2)
ax2.set_title("Barplot: Rata-rata Jumlah Peminjaman per Kondisi Cuaca")
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Jumlah Peminjaman")
st.pyplot(fig2)

# 3. Scatterplot: Hubungan suhu (temp) dengan jumlah peminjaman, diwarnai berdasarkan kondisi cuaca
fig3, ax3 = plt.subplots(figsize=(8,6))
sns.scatterplot(x='temp', y='cnt', hue='weathersit', data=filtered_df, ax=ax3)
ax3.set_title("Scatterplot: Suhu vs Jumlah Peminjaman Sepeda")
ax3.set_xlabel("Suhu (temp)")
ax3.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig3)

# ========================
# Section 2: Pengaruh Musim
# ========================
st.header("Pertanyaan 2: Pengaruh Musim terhadap Pola Peminjaman Sepeda")

# 1. Boxplot: Distribusi jumlah peminjaman berdasarkan musim
fig4, ax4 = plt.subplots(figsize=(8,6))
sns.boxplot(x='season_label', y='cnt', data=filtered_df, ax=ax4)
ax4.set_title("Boxplot: Jumlah Peminjaman Berdasarkan Musim")
ax4.set_xlabel("Musim")
ax4.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig4)

# 2. Line Chart: Pola peminjaman per jam untuk setiap musim
hourly_season_agg = filtered_df.groupby(['season_label', 'hr']).agg(average_rentals=('cnt', 'mean')).reset_index()
fig5, ax5 = plt.subplots(figsize=(12,6))
sns.lineplot(x='hr', y='average_rentals', hue='season_label', data=hourly_season_agg, ci=None, ax=ax5)
ax5.set_title("Line Chart: Pola Peminjaman per Jam Berdasarkan Musim")
ax5.set_xlabel("Jam")
ax5.set_ylabel("Rata-rata Jumlah Peminjaman")
st.pyplot(fig5)

# 3. Scatterplot: Hubungan kelembapan (hum) dengan jumlah peminjaman, berdasarkan musim
fig6, ax6 = plt.subplots(figsize=(8,6))
sns.scatterplot(x='hum', y='cnt', hue='season_label', data=filtered_df, ax=ax6)
ax6.set_title("Scatterplot: Kelembapan vs Jumlah Peminjaman Berdasarkan Musim")
ax6.set_xlabel("Kelembapan (hum)")
ax6.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig6)

# 4. Barplot: Rata-rata peminjaman berdasarkan kombinasi musim dan kondisi cuaca
weather_season_agg = filtered_df.groupby(['weathersit', 'season_label']).agg(average_rentals=('cnt', 'mean')).reset_index()
fig7, ax7 = plt.subplots(figsize=(10,6))
sns.barplot(x='season_label', y='average_rentals', hue='weathersit', data=weather_season_agg, ci=None, ax=ax7)
ax7.set_title("Barplot: Rata-rata Peminjaman Berdasarkan Musim dan Kondisi Cuaca")
ax7.set_xlabel("Musim")
ax7.set_ylabel("Rata-rata Jumlah Peminjaman")
st.pyplot(fig7)

st.markdown("""
**Insight Utama:**
- **Cuaca:** Kondisi cuaca cerah (weathersit = 1) menghasilkan jumlah peminjaman yang lebih tinggi, sedangkan kondisi hujan atau salju (weathersit = 3 dan 4) secara signifikan menurunkan peminjaman.
- **Musim:** Musim Fall dan Summer mencatat jumlah peminjaman tertinggi dengan pola harian yang stabil, sedangkan musim Spring dan Winter menunjukkan peminjaman yang lebih rendah.
""")

st.markdown("""
**Conclusion**
- Berdasarkan analisis dan visualisasi data, dapat disimpulkan bahwa kondisi cuaca sangat berpengaruh terhadap jumlah peminjaman sepeda. Hari-hari dengan cuaca cerah (weathersit = 1) menunjukkan rata-rata peminjaman yang jauh lebih tinggi, sedangkan kondisi hujan atau salju (weathersit 3 dan 4) menyebabkan penurunan tajam dalam peminjaman. Visualisasi seperti boxplot dan scatterplot mengungkapkan hubungan positif antara suhu dan peminjaman, yang menunjukkan bahwa faktor cuaca merupakan elemen krusial dalam menentukan permintaan. Oleh karena itu, strategi operasional dan promosi harus disesuaikan dengan kondisi cuaca untuk mengoptimalkan penggunaan armada sepeda dan meningkatkan kepuasan pelanggan.
- Analisis musiman mengungkapkan bahwa musim memiliki peran penting dalam pola peminjaman sepeda. Data menunjukkan bahwa musim Fall dan Summer mencatat jumlah peminjaman tertinggi dengan pola harian yang stabil, sementara musim Spring cenderung menghasilkan peminjaman yang lebih rendah. Visualisasi melalui line chart per jam dan boxplot memperlihatkan perbedaan tren peminjaman antar musim, yang mengindikasikan perlunya penyesuaian jadwal operasional dan promosi sesuai dengan periode musiman. Dengan memahami variasi ini, pengelola layanan dapat mengoptimalkan alokasi sumber daya, meningkatkan efisiensi operasional, dan merancang strategi pemasaran yang lebih tepat sasaran.""")
# Bike Sharing Dashboard

Proyek ini adalah sebuah **dashboard interaktif** berbasis Streamlit yang digunakan untuk menganalisis data bike sharing. Dashboard ini mengeksplorasi pengaruh cuaca dan musim terhadap jumlah peminjaman sepeda melalui berbagai visualisasi seperti boxplot, barplot, scatterplot, dan line chart.

## Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Running the Dashboard Locally](#running-the-dashboard-locally)
- [Deployment](#deployment)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Overview

Dashboard ini dibuat untuk membantu memahami bagaimana kondisi cuaca dan variasi musiman mempengaruhi peminjaman sepeda. Dengan menggunakan data historis yang telah dikumpulkan, dashboard menyediakan insight seperti:
- Pengaruh cuaca terhadap jumlah peminjaman sepeda.
- Pola peminjaman berdasarkan musim.
- Hubungan antara suhu, kelembapan, dan jumlah peminjaman.


**Catatan:**  
- Jika kamu ingin menggunakan data lain dari folder `data/`, sesuaikan path di kode kamu.

## Installation

1. **Clone repository:**
   ```bash
   git clone https://github.com/julioaldprb/submission-dicoding.git
   cd submission-dicoding/dashboard

2.  Buat dan aktifkan virtual environment
- Windows
    ````bash
    Copy
    Edit
    python -m venv venv
    venv\Scripts\activate

- macOS/Linux:
    ```bash
    Copy
    Edit
    python3 -m venv venv
    source venv/bin/activate

3. Install dependensi:
    ```bash
    Copy
    Edit
    pip install -r ../requirements.txt

### Running the Dashboard Locally
Jalankan dashboard dengan perintah:

    ```bash
    Copy
    Edit
    streamlit run dashboard.py
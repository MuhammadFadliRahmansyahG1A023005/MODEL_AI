# 🚦 SmartCity Bengkulu - Prediksi Lalu Lintas Bengkulu
Ini adalah kode untuk  **prediksi dan visualisasi lalu lintas berbasis web** di Bengkulu. 🗺️🚗

## 👥 Anggota Kelompok 9

| Nama                     | GitHub                                      |
|--------------------------|---------------------------------------------|
| Muhammad Fadli Rahmansyah | [MuhammadFadliRahmansyahG1A023005](https://github.com/MuhammadFadliRahmansyahG1A023005)  |
| Hana Syarifah   | [HanaSyarifahG1A023017](https://github.com/HanaSyarifahG1A023017?authuser=0)    |
| jundi Al farros   | [alfarros](https://github.com/alfarros)    |

### Yang Akan Ditampilkan Kode Ini ✨

1.  **Peta Interaktif Bengkulu**: Sebuah peta dinamis yang menampilkan lokasi-lokasi penting seperti landmark (misalnya, Benteng Marlborough 🏰) dan penanda untuk jalan-jalan utama yang datanya kami pantau. 📍
2.  **Formulir Prediksi Lalu Lintas**: Pengguna dapat memilih nama jalan, jam 🕒, hari 🗓️, dan kondisi cuaca ⛈️ untuk mendapatkan prediksi kemacetan.
3.  **Hasil Prediksi Kemacetan**: Setelah formulir disubmit, aplikasi akan menampilkan:
    * Tingkat kemacetan yang diprediksi (misalnya, "Normal" ✅, "Padat" 🟠, "Macet" ⛔).
    * Perkiraan jumlah kendaraan yang lewat dan persentase kapasitas jalan yang digunakan.
    * **Rekomendasi Rute Alternatif**: Jika jalan utama diprediksi macet, aplikasi akan menyarankan jalur lain yang mungkin lebih lancar. 🔄
Baik, mari kita bedah kelebihan dan kekurangan dari kode aplikasi prediksi lalu lintas ini.

---

### Kelebihan model Ini ✅

1.  **Struktur Kode yang Jelas dan Modular**
2.  **Menggunakan Flask Framework yang Ringan**
3.  **Visualisasi Peta Interaktif dengan Folium**
4.  **Simulasi Prediksi Lalu Lintas yang Dapat Disesuaikan**
5.  **Penyediaan Rute Alternatif (Secara Data)**
6.  **Pembaruan Waktu Nyata (Current Time)**
7.  **Informasi Lalu Lintas "Saat Ini" (Dummy Data)**
   
### Kekurangan model Ini ❌
1.  **Model Prediksi yang Sangat Sederhana (Rule-Based)**
2.  **Data Lalu Lintas "Current" dan "Predicted" adalah Dummy**
3.  **Visualisasi Peta yang Kurang Informatif untuk Lalu Lintas**
4.  **Keterbatasan Skalabilitas Data Jalan**
5.  **Tidak Ada Interaksi Peta yang Lebih Dalam**
6.  **Ketergantungan pada Input Manual**
7.  **Tidak Ada Validasi Input yang Kuat**

Tentu, mari kita kemas informasi tentang model AI yang digunakan dalam proyek Anda agar lebih menarik di GitHub!

---

## Intip "Otak" di Balik Prediksi Lalu Lintas Kami: Model Berbasis Aturan yang Efisien 🧠

Meskipun aplikasi kami menyajikan prediksi lalu lintas yang informatif, penting untuk memahami "model" di baliknya. Kami menggunakan pendekatan **model berbasis aturan (rule-based)** atau **heuristik yang disimulasikan**, bukan model Machine Learning (ML) kompleks seperti Neural Network atau Decision Tree.

Kode yang menunjukkan model ini berbasis aturan adalah seluruh logika di dalam fungsi calculate_traffic_prediction.
def calculate_traffic_prediction(road_name, hour, day, weather):
    """Menghitung perkiraan volume lalu lintas berdasarkan input."""
    road_info = ROAD_DATA.get(road_name, {})
    capacity = road_info.get("capacity", 1000)
     
    base_volume = capacity * 0.6  # <--- Aturan Dasar: Volume awal adalah 60% dari kapasitas

    # Pengaruh waktu puncak
    if 7 <= hour <= 9 or 16 <= hour <= 18:  # <--- Aturan 1: Jika jam sibuk pagi (7-9) atau sore (16-18)
        base_volume *= 1.3  # <--- Pengali: Tambah volume 30%
    elif 12 <= hour <= 14: # <--- Aturan 2: Jika jam makan siang (12-14)
        base_volume *= 1.1  # <--- Pengali: Tambah volume 10%

    # Pengaruh hari kerja/libur
    if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]: # <--- Aturan 3: Jika hari kerja
        base_volume *= 1.1  # <--- Pengali: Tambah volume 10%
    elif day in ["Saturday"]: # <--- Aturan 4: Jika hari Sabtu
        base_volume *= 1.05  # <--- Pengali: Tambah volume 5%

    # Pengaruh cuaca
    if weather == "Hujan": # <--- Aturan 5: Jika cuaca Hujan
        base_volume *= 1.15  # <--- Pengali: Tambah volume 15%
    elif weather == "Hujan Lebat": # <--- Aturan 6: Jika cuaca Hujan Lebat
        base_volume *= 1.3  # <--- Pengali: Tambah volume 30%

    predicted_vehicle_count = int(base_volume)
    percentage_capacity = (predicted_vehicle_count / capacity) * 100

    congestion_level, congestion_color = "Normal", "green"
    if percentage_capacity >= 100: # <--- Aturan 7: Jika >= 100% kapasitas
        congestion_level, congestion_color = "Macet", "red"
    elif percentage_capacity >= 80: # <--- Aturan 8: Jika >= 80% kapasitas
        congestion_level, congestion_color = "Sangat Padat", "red"
    elif percentage_capacity >= 60: # <--- Aturan 9: Jika >= 60% kapasitas
        congestion_level, congestion_color = "Padat", "orange"
     
    return predicted_vehicle_count, capacity, percentage_capacity, congestion_level, congestion_color

### Mengapa Memilih Model Berbasis Aturan? 🤔

Pemilihan model ini didasari oleh beberapa pertimbangan strategis yang berfokus pada efisiensi dan tujuan proyek kami:

* **Kesederhanaan & Implementasi Cepat** ✨
Model ini sangat mudah dipahami dan diimplementasikan tanpa perlu data pelatihan yang besar atau algoritma ML yang rumit. Kami tidak memerlukan proses *training* atau *tuning* model yang intensif, memungkinkan pengembangan yang lebih gesit.
* **Fokus pada Demonstrasi & Visualisasi** 🗺️
   Tujuan utama proyek ini adalah mendemonstrasikan konsep prediksi lalu lintas dan visualisasi peta interaktif di Bengkulu. Model berbasis aturan sudah sangat memadai untuk memberikan gambaran realistis tentang bagaimana berbagai faktor memengaruhi arus kendaraan. Fokus kami lebih pada antarmuka web yang intuitif dan visualisasi data yang menarik, bukan pada akurasi prediksi tingkat militer.
* **Keterbatasan Data Real-time** 🚧
     Dalam konteks proyek ini, kami tidak mengintegrasikan sumber data lalu lintas *real-time* atau historis yang ekstensif. Data yang digunakan bersifat simulasi atau "dummy". Tanpa data sungguhan yang besar dan bervariasi, penggunaan model AI/ML yang lebih canggih tidak akan efektif dan justru menambah kompleksitas yang tidak perlu.

---

### Bagaimana Model Berbasis Aturan Kami Bekerja? ⚙️

Inti dari "otak" prediksi kami ada pada fungsi `calculate_traffic_prediction`. Berikut cara kerjanya:

1.  **Volume Dasar**: Pertama, model mengambil volume dasar kendaraan berdasarkan **kapasitas maksimum** setiap jalan.
2.  **Aplikasi Aturan Pengali**: Kemudian, serangkaian aturan diterapkan dalam bentuk **pengali (multiplier)** untuk menyesuaikan volume dasar tersebut berdasarkan faktor-faktor kunci yang Anda masukkan:
    * **Jam 🕒**: Lalu lintas diprediksi lebih padat pada jam sibuk (misalnya, pagi dan sore hari).
    * **Hari 🗓️**: Hari kerja cenderung memiliki volume lalu lintas yang lebih tinggi dibanding akhir pekan.
    * **Cuaca ⛈️**: Kondisi cuaca buruk, seperti hujan atau hujan lebat, secara signifikan dapat memperlambat arus lalu lintas, sehingga volume kendaraan yang terasa memadati jalan akan lebih tinggi.
3.  **Penentuan Tingkat Kemacetan**: Hasil perhitungan volume kendaraan yang diprediksi kemudian dibandingkan dengan kapasitas jalan untuk menentukan **tingkat kemacetan** (Normal, Padat, Sangat Padat, Macet Total) dan **warna indikator** yang sesuai (hijau, oranye, merah). Ambang batas ini telah ditetapkan secara *hardcoded* dalam kode.

Dengan pendekatan ini, kami berhasil menciptakan sebuah sistem yang fungsional dan mudah dipahami, ideal untuk mendemonstrasikan potensi prediksi lalu lintas di Bengkulu! ✨

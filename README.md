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


### Diagram Alur Sistem
<img src="https://github.com/MuhammadFadliRahmansyahG1A023005/MODEL_AI/blob/main/Gambar%20WhatsApp%202025-06-08%20pukul%2019.45.19_ae3b3724.jpg" width="400"/>

### Bagaimana Model Berbasis Aturan Kami Bekerja? ⚙️

Inti dari "otak" prediksi kami ada pada fungsi `calculate_traffic_prediction`. Berikut cara kerjanya:

1.  **Volume Dasar**: Pertama, model mengambil volume dasar kendaraan berdasarkan **kapasitas maksimum** setiap jalan.
2.  **Aplikasi Aturan Pengali**: Kemudian, serangkaian aturan diterapkan dalam bentuk **pengali (multiplier)** untuk menyesuaikan volume dasar tersebut berdasarkan faktor-faktor kunci yang Anda masukkan:
    * **Jam 🕒**: Lalu lintas diprediksi lebih padat pada jam sibuk (misalnya, pagi dan sore hari).
    * **Hari 🗓️**: Hari kerja cenderung memiliki volume lalu lintas yang lebih tinggi dibanding akhir pekan.
    * **Cuaca ⛈️**: Kondisi cuaca buruk, seperti hujan atau hujan lebat, secara signifikan dapat memperlambat arus lalu lintas, sehingga volume kendaraan yang terasa memadati jalan akan lebih tinggi.
3.  **Penentuan Tingkat Kemacetan**: Hasil perhitungan volume kendaraan yang diprediksi kemudian dibandingkan dengan kapasitas jalan untuk menentukan **tingkat kemacetan** (Normal, Padat, Sangat Padat, Macet Total) dan **warna indikator** yang sesuai (hijau, oranye, merah). Ambang batas ini telah ditetapkan secara *hardcoded* dalam kode.

## 🗂️ Jenis & Sumber Data

Aplikasi ini mengintegrasikan berbagai jenis data untuk memberikan informasi dan prediksi lalu lintas. Berikut adalah rincian jenis dan sumber data yang digunakan:

### 2.1 Data Lalu Lintas

* **Jenis Data:** Data volume kendaraan, kapasitas jalan, dan tingkat kemacetan.
* **Sumber Data:**
    * **Simulasi Internal:** Untuk tujuan pengembangan dan demonstrasi awal, data lalu lintas historis yang digunakan untuk melatih model AI (`traffic_model.pkl`) saat ini adalah **data simulasi** yang dihasilkan oleh skrip `train_model.py`. Simulasi ini mempertimbangkan faktor-faktor seperti kapasitas jalan, jam sibuk, hari dalam seminggu, dan kondisi cuaca untuk menciptakan pola yang mendekati perilaku lalu lintas.
    * **Data Statis (CURRENT_TRAFFIC_DATA):** Data lalu lintas "terkini" yang ditampilkan di peta (`CURRENT_TRAFFIC_DATA` di `app.py`) adalah **data dummy statis** yang dibuat secara manual. Data ini mencakup nama jalan, perkiraan jumlah kendaraan, kapasitas, cuaca, tingkat kemacetan, dan koordinat geografis.

### 2.2 Data Lokasi Geografis

* **Jenis Data:** Koordinat lintang (latitude) dan bujur (longitude) serta nama-nama tempat.
* **Sumber Data:**
    * **Titik Penting (IMPORTANT_LOCATIONS):** Data koordinat untuk lokasi-lokasi penting di Bengkulu (seperti Benteng Marlborough, Masjid Jamik, dll.) adalah **data statis yang didefinisikan secara manual** di dalam file `app.py`.
    * **Jalan dan Rute Alternatif (ROAD_DATA):** Koordinat titik-titik (polyline) yang membentuk jalur jalan utama dan rute alternatif, beserta kapasitas jalan, juga merupakan **data statis yang didefinisikan secara manual** di dalam `app.py`. Meskipun rute ini tidak digambar secara visual di peta saat ini, data koordinatnya tersedia untuk potensi pengembangan visualisasi rute.

### 2.3 Data Cuaca

* **Jenis Data:** Kondisi cuaca (Cerah, Berawan, Hujan, Hujan Lebat).
* **Sumber Data:**
    * **Simulasi Internal:** Dalam `train_model.py`, kondisi cuaca adalah **fitur yang disimulasikan secara acak** untuk melatih model.
    * **Input Pengguna:** Dalam antarmuka web, kondisi cuaca adalah **input yang dipilih oleh pengguna** untuk prediksi lalu lintas.
    * **Data Statis (CURRENT_TRAFFIC_DATA):** Kondisi cuaca untuk data lalu lintas "terkini" juga **didefinisikan secara statis**.

**Catatan Pengembangan Lanjutan:**
Seperti yang disorot di bagian "Pengembangan Lanjutan", untuk implementasi dunia nyata, sumber data ini perlu ditingkatkan secara signifikan dengan mengintegrasikan API data lalu lintas dan cuaca real-time, serta data historis yang sebenarnya.

### ⚙️ Data Latih Model

Model prediksi lalu lintas dalam program ini dilatih menggunakan data historis. Untuk keperluan demonstrasi dan mempermudah replikasi awal, data historis ini **disimulasikan** dalam skrip `train_model.py`.

#### Fitur yang Digunakan untuk Pelatihan:

Model Random Forest Regressor belajar dari pola-pola berikut untuk memprediksi volume kendaraan:

* **`road_name`**: Nama jalan yang akan diprediksi lalu lintasnya (misalnya, "Jalan Suprapto", "Jalan Sudirman"). Ini adalah fitur kategorikal.
* **`hour`**: Jam dalam sehari (0-23). Ini adalah fitur numerik.
* **`day_of_week`**: Hari dalam seminggu (misalnya, "Monday", "Tuesday", ..., "Sunday"). Ini adalah fitur kategorikal.
* **`weather`**: Kondisi cuaca saat itu (misalnya, "Cerah", "Berawan", "Hujan", "Hujan Lebat"). Ini adalah fitur kategorikal.

#### Target Prediksi:

* **`predicted_vehicle_count`**: Jumlah kendaraan yang diperkirakan akan berada di jalan pada waktu dan kondisi tertentu. Ini adalah variabel numerik yang merupakan target prediksi model.

#### Simulasi Data:

Dalam `train_model.py`, data historis disimulasikan berdasarkan logika sederhana yang mempertimbangkan:
* **Kapasitas Jalan:** Setiap jalan memiliki kapasitas maksimum.
* **Jam Sibuk (Rush Hour):** Volume lalu lintas lebih tinggi pada jam-jam sibuk pagi dan sore.
* **Hari Kerja/Akhir Pekan:** Pola lalu lintas berbeda antara hari kerja dan akhir pekan.
* **Kondisi Cuaca:** Cuaca buruk (hujan) dapat meningkatkan volume atau kepadatan lalu lintas.
* **Noise:** Ditambahkan sedikit *noise* acak untuk membuat data lebih realistis dan tidak terlalu "sempurna".

**Penting:**
Untuk aplikasi dunia nyata, sangat disarankan untuk mengganti data simulasi ini dengan **data historis lalu lintas yang sesungguhnya** yang dikumpulkan dari sensor, GPS, atau sumber data lalu lintas lainnya. Menggunakan data riil akan secara signifikan meningkatkan akurasi dan relevansi prediksi model.

## 🔄 Alur Kerja Sistem

Sistem Smart City Traffic Prediction ini mengikuti alur kerja yang logis, dimulai dari pelatihan model hingga penyajian informasi dan prediksi kepada pengguna melalui antarmuka web.

### 3.1 Alur Pelatihan Model (`train_model.py`)

1.  **Pengambilan/Simulasi Data Historis:**
    * Skrip `train_model.py` memulai dengan mensimulasikan data lalu lintas historis. Data ini mencakup `road_name`, `hour`, `day_of_week`, dan `weather` sebagai fitur, serta `predicted_vehicle_count` sebagai target.
    * (Dalam implementasi dunia nyata, ini akan menjadi tahap di mana data historis riil dikumpulkan dari berbagai sumber seperti sensor lalu lintas, GPS, dll.)

2.  **Preprocessing Data:**
    * Data historis yang disimulasikan kemudian melalui tahap *preprocessing*.
    * Fitur kategorikal (`road_name`, `day_of_week`, `weather`) dikodekan menggunakan `OneHotEncoder` agar dapat diproses oleh model.
    * Fitur numerik (`hour`) distandarisasi menggunakan `StandardScaler` untuk memastikan skala yang seragam.
    * Proses *preprocessing* ini dienkapsulasi dalam `ColumnTransformer` dan `Pipeline` dari Scikit-learn.

3.  **Pelatihan Model Machine Learning:**
    * Model *Random Forest Regressor* diinisialisasi dan dilatih menggunakan data yang telah diproses.
    * Model belajar hubungan antara fitur-fitur (jalan, waktu, hari, cuaca) dan volume lalu lintas yang dihasilkan.

4.  **Evaluasi Model:**
    * Setelah pelatihan, model dievaluasi menggunakan $R^2$ Score pada data pelatihan dan data pengujian untuk mengukur kinerjanya.

5.  **Penyimpanan Model:**
    * Model yang telah dilatih kemudian disimpan sebagai file `traffic_model.pkl` menggunakan `joblib`. File ini akan dimuat oleh aplikasi web untuk melakukan prediksi.

### 3.2 Alur Aplikasi Web (`app.py`)

1.  **Inisialisasi Aplikasi Flask:**
    * Saat `app.py` dijalankan, aplikasi web Flask dimulai.
    * Model AI yang telah dilatih (`traffic_model.pkl`) dimuat ke dalam memori untuk digunakan dalam prediksi. Jika model tidak ditemukan atau gagal dimuat, sistem akan *fallback* ke logika prediksi berbasis aturan manual.

2.  **Penyajian Halaman Utama:**
    * Ketika pengguna mengakses URL utama (`/`), fungsi `index()` dipanggil.
    * Peta interaktif Folium dibuat, berpusat di Bengkulu.
    * Lokasi-lokasi penting (`IMPORTANT_LOCATIONS`) ditambahkan ke peta sebagai marker.
    * Data lalu lintas "terkini" (`CURRENT_TRAFFIC_DATA`, yang merupakan data statis dummy) juga ditambahkan ke peta sebagai marker jalan dengan warna yang menunjukkan tingkat kemacetan.
    * Legenda kustom ditambahkan ke peta.
    * Halaman `index.html` dirender dan dikirim ke browser pengguna, termasuk peta yang sudah dihasilkan.

3.  **Proses Prediksi Lalu Lintas (Saat Form Disubmit):**
    * Pengguna memilih `road_name`, `hour`, `day`, dan `weather` dari form di antarmuka web.
    * Ketika form disubmit (`POST` request), data input diambil.
    * Fungsi `predict_traffic_with_ai()` dipanggil dengan input pengguna.
    * Input pengguna diproses (disiapkan dalam format DataFrame) dan diberikan kepada model AI yang sudah dimuat (`traffic_prediction_model.predict()`).
    * Model menghasilkan prediksi `predicted_vehicle_count`.
    * Berdasarkan prediksi ini dan kapasitas jalan, tingkat kemacetan (`congestion_level`) dan warna (`congestion_color`) dihitung.
    * Informasi rute alternatif untuk jalan yang dipilih juga diambil dari `ROAD_DATA`.

4.  **Tampilan Hasil Prediksi:**
    * Hasil prediksi (jumlah kendaraan, tingkat kemacetan, rute alternatif yang disarankan) ditampilkan kembali di halaman web.
    * Peta diperbarui (atau diregenerasi) dengan informasi lalu lintas terkini dan form prediksi siap untuk input berikutnya.

## Pengujian aplikasi 
> Pengujian dilakukan dengan studi kasus yaitu melakukan pencarian rute dan prediksi kemacetan dan alternatif jalan
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">

   <img src="https://github.com/MuhammadFadliRahmansyahG1A023005/MODEL_AI/blob/main/Cuplikan%20layar%202025-06-08%20183917.png" width="180"/>
   <img src="https://github.com/MuhammadFadliRahmansyahG1A023005/MODEL_AI/blob/main/Cuplikan%20layar%202025-06-08%20183933.png" width="180"/>
   <img src="https://github.com/MuhammadFadliRahmansyahG1A023005/MODEL_AI/blob/main/Cuplikan%20layar%202025-06-08%20183945.png" width="180"/>
   <img src="https://github.com/MuhammadFadliRahmansyahG1A023005/MODEL_AI/blob/main/Cuplikan%20layar%202025-06-08%20184045.png" width="180"/>
   <img src="https://github.com/MuhammadFadliRahmansyahG1A023005/MODEL_AI/blob/main/Cuplikan%20layar%202025-06-08%20184104.png" width="180"/>

## 🚀 Pengembangan Lanjutan
> Proyek Smart City Traffic Prediction ini adalah titik awal yang kuat untuk sistem manajemen lalu lintas cerdas. Ada banyak area untuk pengembangan dan peningkatan lebih lanjut untuk menjadikannya lebih akurat, komprehensif, dan siap produksi:

1. Peningkatan Model Prediksi Lalu Lintas
Data Historis Riil: Ganti data lalu lintas simulasi di train_model.py dengan dataset historis lalu lintas yang sesungguhnya (misalnya, dari sensor lalu lintas, GPS kendaraan, atau sumber data kota). Ini adalah langkah paling krusial untuk meningkatkan akurasi prediksi secara signifikan.
Fitur Tambahan:
Acara Khusus/Liburan: Integrasikan data tentang acara besar (konser, festival), hari libur nasional, atau cuti bersama yang dapat memengaruhi pola lalu lintas.
Kecelakaan/Insiden: Sertakan data insiden lalu lintas real-time atau historis untuk memprediksi dampaknya.
Fase Lampu Lalu Lintas: Jika tersedia, integrasikan informasi tentang durasi fase lampu lalu lintas.
Jenis Hari (Kerja/Libur): Meskipun sudah ada day_of_week, bisa lebih spesifik seperti 'Hari Kerja', 'Akhir Pekan', 'Hari Libur Nasional'.
Algoritma yang Lebih Kompleks: Eksplorasi algoritma Machine Learning yang lebih canggih atau model Deep Learning seperti:
LSTM (Long Short-Term Memory) atau GRU: Sangat cocok untuk data deret waktu seperti lalu lintas, karena dapat menangkap dependensi temporal.
Graph Neural Networks (GNN): Jika data topologi jalan tersedia, GNN bisa memodelkan hubungan antar jalan dengan lebih baik.
XGBoost / LightGBM: Algoritma gradient boosting yang dikenal sangat efisien dan akurat.
Penyesuaian Hiperparameter: Lakukan hyperparameter tuning yang lebih mendalam pada model Random Forest atau model lain yang dipilih untuk mengoptimalkan kinerjanya (misalnya, menggunakan GridSearchCV atau RandomizedSearchCV).
Validasi Model yang Lebih Kuat: Terapkan teknik validasi silang (k-fold cross-validation) untuk mendapatkan estimasi kinerja model yang lebih robust.
2. Peningkatan Data Real-time dan Integrasi API
Integrasi Data Lalu Lintas Real-time: Dapatkan data lalu lintas dari API penyedia peta (misalnya, Google Maps Traffic API, OpenStreetMap, HERE Technologies) untuk kondisi lalu lintas yang lebih akurat dan dinamis.
Integrasi Data Cuaca Real-time: Ambil data cuaca dari API cuaca (misalnya, OpenWeatherMap, AccuWeather) untuk mendapatkan kondisi cuaca aktual.
Integrasi Sensor: Jika ada, hubungkan dengan sensor lalu lintas fisik (induktif loop, kamera) yang terpasang di jalan.
3. Peningkatan Antarmuka Pengguna (UI) dan Peta
Visualisasi Rute Lalu Lintas: Gambar jalur jalan yang sebenarnya (polyline) di peta Folium dengan warna yang menunjukkan tingkat kemacetan. Saat ini, hanya marker nama jalan yang ditambahkan.
Visualisasi Rute Alternatif: Tampilkan rute alternatif yang disarankan langsung di peta saat pengguna memilih opsi prediksi.
Pembaruan Peta Otomatis: Perbarui data lalu lintas di peta secara otomatis setiap beberapa menit tanpa perlu memuat ulang halaman.
Fungsionalitas Pencarian/Filter: Tambahkan kolom pencarian untuk lokasi penting atau jalan.
Tampilan Detail Lalu Lintas: Pop-up atau panel yang lebih kaya saat mengklik jalan, menampilkan detail prediksi, riwayat kemacetan singkat, atau rute alternatif terdekat.
Desain UI/UX yang Lebih Baik: Perbaiki tata letak, gaya, dan responsivitas halaman web untuk pengalaman pengguna yang lebih intuitif dan modern.
4. Optimalisasi Rute dan Rekomendasi
Algoritma Penentuan Rute: Kembangkan algoritma penentuan rute yang memperhitungkan prediksi kemacetan untuk menyarankan jalur tercepat atau paling tidak macet (misalnya, Dijkstra's Algorithm atau A* dengan bobot dinamis berdasarkan prediksi lalu lintas).
Integrasi Origin-Destination: Tambahkan fitur di mana pengguna dapat memasukkan titik awal dan tujuan, dan sistem akan merekomendasikan rute optimal.
5. Skalabilitas dan Deployment
Database: Ganti penyimpanan data saat ini (list/dictionary Python) dengan database yang lebih skalabel (misalnya, PostgreSQL, MongoDB) untuk menyimpan data historis lalu lintas, lokasi, dan konfigurasi jalan.
Deployment: Siapkan aplikasi untuk deployment ke lingkungan produksi (misalnya, dengan Gunicorn/Nginx, Docker, atau platform cloud seperti Heroku, AWS Elastic Beanstalk, Google Cloud Run) untuk ketersediaan 24/7.
API Endpoint: Buat API endpoint terpisah untuk prediksi lalu lintas, sehingga dapat diintegrasikan dengan aplikasi lain (misalnya, aplikasi mobile).
6. Fitur Tambahan Potensial
Pemberitahuan/Alerts: Sistem peringatan untuk kemacetan parah atau insiden tak terduga.
Manajemen Lampu Lalu Lintas Cerdas: Jika terhubung ke infrastruktur kota, sistem dapat menyarankan perubahan fase lampu lalu lintas berdasarkan prediksi kemacetan.
Dashboard Analitik: Buat dashboard yang lebih mendalam untuk menganalisis tren lalu lintas, pola kemacetan, dan kinerja model.

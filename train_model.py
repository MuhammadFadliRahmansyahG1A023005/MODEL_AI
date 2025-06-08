import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import random

# --- Konfigurasi Data (Diambil dari ROAD_DATA di app.py) ---
# Diperlukan untuk simulasi data historis agar konsisten dengan kapasitas jalan
ROAD_DATA = {
    "Jalan Suprapto": {"capacity": 1000},
    "Jalan Sudirman": {"capacity": 1200},
    "Jalan P. Natadirja": {"capacity": 800},
    "Jalan Adam Malik": {"capacity": 900},
    "Jalan WR Supratman": {"capacity": 1050},
    "Jalan Bhayangkara": {"capacity": 950},
    "Jalan Putri Gading Cempaka": {"capacity": 1100},
    "Jalan KZ Abidin": {"capacity": 850},
    "Jalan Fatmawati": {"capacity": 800},
    "Jalan Ahmad Yani": {"capacity": 1200},
    "Jalan S. Parman": {"capacity": 900},
}


# --- Simulasi Data Historis ---
# Anda harus mengganti ini dengan data lalu lintas historis RIIL
# untuk akurasi yang lebih baik di dunia nyata.
n_samples = 5000
road_names_list = list(ROAD_DATA.keys())
days_of_week_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weather_conditions_list = ["Cerah", "Berawan", "Hujan", "Hujan Lebat"]

data = {
    'road_name': random.choices(road_names_list, k=n_samples),
    'hour': np.random.randint(0, 24, n_samples),
    'day_of_week': random.choices(days_of_week_list, k=n_samples),
    'weather': random.choices(weather_conditions_list, k=n_samples)
}
df = pd.DataFrame(data)

# Hitung predicted_vehicle_count berdasarkan aturan yang disimulasikan
# Ini meniru logika Anda sebelumnya, tapi sekarang menjadi "data historis"
# untuk model AI untuk belajar.
def simulate_traffic_prediction(row):
    road_info = ROAD_DATA.get(row['road_name'], {})
    capacity = road_info.get("capacity", 1000)
    base_volume = capacity * 0.6

    if 7 <= row['hour'] <= 9 or 16 <= row['hour'] <= 18:
        base_volume *= 1.3
    elif 12 <= row['hour'] <= 14:
        base_volume *= 1.1

    if row['day_of_week'] in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        base_volume *= 1.1
    elif row['day_of_week'] in ["Saturday"]:
        base_volume *= 1.05

    if row['weather'] == "Hujan":
        base_volume *= 1.15
    elif row['weather'] == "Hujan Lebat":
        base_volume *= 1.3

    # Tambahkan sedikit noise agar tidak terlalu sempurna
    noise = np.random.normal(0, capacity * 0.05) # 5% dari kapasitas sebagai noise
    return max(0, int(base_volume + noise))

df['predicted_vehicle_count'] = df.apply(simulate_traffic_prediction, axis=1)

# --- Preprocessing dan Pelatihan Model AI ---

# Definisikan fitur kategorikal dan numerik
categorical_features = ['road_name', 'day_of_week', 'weather']
numerical_features = ['hour']

# Buat pipeline preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Buat pipeline model (Preprocessor + Random Forest Regressor)
# Kita memprediksi predicted_vehicle_count (masalah regresi)
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Definisikan fitur (X) dan target (y)
X = df[['road_name', 'hour', 'day_of_week', 'weather']]
y = df['predicted_vehicle_count']

# Bagi data menjadi training dan testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Latih model
print("Melatih model AI...")
model_pipeline.fit(X_train, y_train)
print("Model AI berhasil dilatih.")

# Evaluasi model (opsional, tapi disarankan)
train_score = model_pipeline.score(X_train, y_train)
test_score = model_pipeline.score(X_test, y_test)
print(f"R^2 Score pada data training: {train_score:.4f}")
print(f"R^2 Score pada data testing: {test_score:.4f}")

# Simpan model yang sudah dilatih
joblib.dump(model_pipeline, 'traffic_model.pkl')
print("Model AI disimpan sebagai 'traffic_model.pkl'")
from flask import Flask, render_template, request
from datetime import datetime
import folium

app = Flask(__name__)

# --- Configuration Data ---
# Data kapasitas jalan dan rute alternatif untuk simulasi
# Path_coords masih ada di sini karena digunakan untuk prediksi rute alternatif di panel,
# meskipun tidak digambar di peta.
ROAD_DATA = {
    "Jalan Suprapto": {
        "capacity": 1000,
        "main_path_coords": [
            [-3.7946, 102.2635], [-3.7940, 102.2638], [-3.7935, 102.2642],
            [-3.7925, 102.2650], [-3.7915, 102.2655], [-3.7905, 102.2660],
            [-3.7895, 102.2665], [-3.7885, 102.2670], [-3.7875, 102.2675],
            [-3.7865, 102.2680], [-3.7855, 102.2685], [-3.7845, 102.2690],
            [-3.7835, 102.2693], [-3.7820, 102.2700]
        ],
        "alternative_routes": [
            {"name": "Jalan Merdeka", "path_coords": [[-3.7946, 102.2635], [-3.7900, 102.2650], [-3.7850, 102.2675], [-3.7800, 102.2700]]},
            {"name": "Jalan Soekarno Hatta", "path_coords": [[-3.7946, 102.2635], [-3.8000, 102.2700], [-3.8050, 102.2750], [-3.8100, 102.2800]]}
        ]
    },
    "Jalan Sudirman": {
        "capacity": 1200,
        "main_path_coords": [
            [-3.7970, 102.2640], [-3.7968, 102.2638], [-3.7965, 102.2635],
            [-3.7960, 102.2630], [-3.7955, 102.2625], [-3.7950, 102.2620]
        ],
        "alternative_routes": [
            {"name": "Jalan S. Parman", "path_coords": [[-3.7970, 102.2640], [-3.7980, 102.2625], [-3.7990, 102.2610]]},
            {"name": "Jalan Fatmawati", "path_coords": [[-3.7970, 102.2640], [-3.7920, 102.2620], [-3.7880, 102.2600]]}
        ]
    },
    "Jalan P. Natadirja": {
        "capacity": 800,
        "main_path_coords": [
            [-3.8010, 102.2590], [-3.8015, 102.2588], [-3.8020, 102.2585],
            [-3.8025, 102.2580], [-3.8030, 102.2578], [-3.8035, 102.2575], [-3.8040, 102.2570]
        ],
        "alternative_routes": [
            {"name": "Jalan Jati", "path_coords": [[-3.8010, 102.2590], [-3.8030, 102.2570], [-3.8050, 102.2550]]},
            {"name": "Jalan Mangga Dua", "path_coords": [[-3.8010, 102.2590], [-3.8080, 102.2595], [-3.8150, 102.2600]]}
        ]
    },
    "Jalan Adam Malik": {
        "capacity": 900,
        "main_path_coords": [
            [-3.7900, 102.2800], [-3.7895, 102.2810], [-3.7890, 102.2820],
            [-3.7885, 102.2830], [-3.7880, 102.2840], [-3.7875, 102.2850],
            [-3.7870, 102.2860], [-3.7865, 102.2870], [-3.7860, 102.2880],
            [-3.7855, 102.2890], [-3.7850, 102.2900]
        ],
        "alternative_routes": [
            {"name": "Jalan Nusa Indah", "path_coords": [[-3.7900, 102.2800], [-3.7875, 102.2850], [-3.7850, 102.2900]]}
        ]
    },
    "Jalan WR Supratman": {
        "capacity": 1050,
        "main_path_coords": [
            [-3.8050, 102.2700], [-3.8048, 102.2704], [-3.8045, 102.2708],
            [-3.8040, 102.2716], [-3.8038, 102.2720], [-3.8035, 102.2724],
            [-3.8030, 102.2732], [-3.8028, 102.2736], [-3.8025, 102.2740]
        ],
        "alternative_routes": [
            {"name": "Jalan Merdeka", "path_coords": [[-3.8050, 102.2700], [-3.7950, 102.2700], [-3.7800, 102.2700]]},
            {"name": "Jalan Soekarno Hatta", "path_coords": [[-3.8050, 102.2700], [-3.8075, 102.2750], [-3.8100, 102.2800]]}
        ]
    },
    "Jalan Bhayangkara": {
        "capacity": 950,
        "main_path_coords": [
            [-3.7850, 102.2550], [-3.7855, 102.2552], [-3.7865, 102.2555],
            [-3.7870, 102.2557], [-3.7880, 102.2560], [-3.7885, 102.2562],
            [-3.7895, 102.2565], [-3.7900, 102.2567], [-3.7910, 102.2570]
        ],
        "alternative_routes": [
            {"name": "Jalan Veteran", "path_coords": [[-3.7850, 102.2550], [-3.7800, 102.2525], [-3.7750, 102.2500]]},
            {"name": "Jalan Ahmad Yani", "path_coords": [[-3.7850, 102.2550], [-3.7885, 102.2560], [-3.7920, 102.2570]]}
        ]
    },
    "Jalan Putri Gading Cempaka": {
        "capacity": 1100,
        "main_path_coords": [
            [-3.8100, 102.2680], [-3.8102, 102.2678], [-3.8105, 102.2675],
            [-3.8108, 102.2672], [-3.8110, 102.2670], [-3.8113, 102.2667],
            [-3.8115, 102.2665], [-3.8118, 102.2662], [-3.8120, 102.2660]
        ],
        "alternative_routes": [
            {"name": "Jalan Salak", "path_coords": [[-3.8100, 102.2680], [-3.8125, 102.2715], [-3.8150, 102.2750]]},
            {"name": "Jalan Bengkulu - Lempuing", "path_coords": [[-3.8100, 102.2680], [-3.8150, 102.2640], [-3.8200, 102.2600]]}
        ]
    },
    "Jalan KZ Abidin": {
        "capacity": 850,
        "main_path_coords": [
            [-3.7900, 102.2750], [-3.7902, 102.2748], [-3.7905, 102.2745],
            [-3.7908, 102.2742], [-3.7910, 102.2740], [-3.7913, 102.2738],
            [-3.7915, 102.2735], [-3.7918, 102.2732], [-3.7920, 102.2730]
        ],
        "alternative_routes": [
            {"name": "Jalan Timur Indah", "path_coords": [[-3.7900, 102.2750], [-3.7875, 102.2800], [-3.7850, 102.2850]]},
            {"name": "Jalan Basuki Rahmat", "path_coords": [[-3.7900, 102.2750], [-3.7950, 102.2725], [-3.8000, 102.2700]]}
        ]
    },
    "Jalan Fatmawati": {
        "capacity": 800,
        "main_path_coords": [
            [-3.7880, 102.2600], [-3.7882, 102.2598], [-3.7885, 102.2596],
            [-3.7888, 102.2594], [-3.7890, 102.2592], [-3.7893, 102.2590],
            [-3.7895, 102.2588], [-3.7898, 102.2586], [-3.7900, 102.2584],
            [-3.7902, 102.2582], [-3.7905, 102.2580]
        ],
        "alternative_routes": [
            {"name": "Jalan Sudirman", "path_coords": [[-3.7880, 102.2600], [-3.7925, 102.2620], [-3.7970, 102.2640]]},
            {"name": "Jalan Raya Kandang Limun", "path_coords": [[-3.7880, 102.2600], [-3.7790, 102.2550], [-3.7700, 102.2500]]}
        ]
    },
    "Jalan Ahmad Yani": {
        "capacity": 1200,
        "main_path_coords": [
            [-3.7920, 102.2570], [-3.7922, 102.2574], [-3.7925, 102.2578],
            [-3.7928, 102.2582], [-3.7930, 102.2586], [-3.7933, 102.2590],
            [-3.7935, 102.2594], [-3.7938, 102.2598], [-3.7940, 102.2602]
        ],
        "alternative_routes": [
            {"name": "Jalan Bhayangkara", "path_coords": [[-3.7920, 102.2570], [-3.7885, 102.2560], [-3.7850, 102.2550]]},
            {"name": "Jalan Suprapto", "path_coords": [[-3.7920, 102.2570], [-3.7933, 102.2600], [-3.7946, 102.2635]]}
        ]
    },
    "Jalan S. Parman": {
        "capacity": 900,
        "main_path_coords": [
            [-3.7990, 102.2610], [-3.7989, 102.2608], [-3.7988, 102.2605],
            [-3.7987, 102.2602], [-3.7986, 102.2600], [-3.7985, 102.2598],
            [-3.7984, 102.2595], [-3.7983, 102.2592], [-3.7982, 102.2590]
        ],
        "alternative_routes": [
            {"name": "Jalan Sudirman", "path_coords": [[-3.7990, 102.2610], [-3.7980, 102.2625], [-3.7970, 102.2640]]},
            {"name": "Jalan Semangka", "path_coords": [[-3.7990, 102.2610], [-3.7995, 102.2555], [-3.8000, 102.2500]]}
        ]
    },
}

# Data dummy untuk kondisi lalu lintas terkini (tambahan koordinat)
CURRENT_TRAFFIC_DATA = [
    {"road_name": "Jalan Suprapto", "predicted_vehicle_count": 850, "capacity": 1000, "weather": "Cerah", "congestion_level": "Normal", "congestion_color": "green", "lat": -3.7946, "lon": 102.2635},
    {"road_name": "Jalan Sudirman", "predicted_vehicle_count": 1100, "capacity": 1200, "weather": "Cerah", "congestion_level": "Padat", "congestion_color": "orange", "lat": -3.7970, "lon": 102.2640},
    {"road_name": "Jalan P. Natadirja", "predicted_vehicle_count": 780, "capacity": 800, "weather": "Hujan", "congestion_level": "Sangat Padat", "congestion_color": "red", "lat": -3.8010, "lon": 102.2590},
    {"road_name": "Jalan WR Supratman", "predicted_vehicle_count": 1575, "capacity": 1050, "weather": "Hujan Lebat", "congestion_level": "Macet", "congestion_color": "red", "lat": -3.8050, "lon": 102.2700},
    {"road_name": "Jalan Bhayangkara", "predicted_vehicle_count": 700, "capacity": 950, "weather": "Cerah", "congestion_level": "Normal", "congestion_color": "green", "lat": -3.7850, "lon": 102.2550},
    {"road_name": "Jalan Putri Gading Cempaka", "predicted_vehicle_count": 950, "capacity": 1100, "weather": "Berawan", "congestion_level": "Padat", "congestion_color": "orange", "lat": -3.8100, "lon": 102.2680},
    {"road_name": "Jalan KZ Abidin", "predicted_vehicle_count": 500, "capacity": 850, "weather": "Cerah", "congestion_level": "Normal", "congestion_color": "green", "lat": -3.7900, "lon": 102.2750},
    {"road_name": "Jalan Fatmawati", "predicted_vehicle_count": 1200, "capacity": 800, "weather": "Cerah", "congestion_level": "Macet", "congestion_color": "red", "lat": -3.7880, "lon": 102.2600},
    {"road_name": "Jalan Ahmad Yani", "predicted_vehicle_count": 1800, "capacity": 1200, "weather": "Berawan", "congestion_level": "Macet", "congestion_color": "red", "lat": -3.7920, "lon": 102.2570},
    {"road_name": "Jalan S. Parman", "predicted_vehicle_count": 1350, "capacity": 900, "weather": "Hujan", "congestion_level": "Macet", "congestion_color": "red", "lat": -3.7990, "lon": 102.2610},
]

# Data titik-titik penting (gedung, objek wisata) di Bengkulu
IMPORTANT_LOCATIONS = [
    {"name": "Benteng Marlborough", "lat": -3.78797, "lon": 102.25244, "icon": "fort-awesome-alt", "color": "darkgreen"},
    {"name": "Masjid Jamik Bengkulu", "lat": -3.79234, "lon": 102.26224, "icon": "mosque", "color": "darkblue"},
    {"name": "Rumah Pengasingan Bung Karno", "lat": -3.79917, "lon": 102.26139, "icon": "home", "color": "orange"},
    {"name": "Tugu Thomas Parr", "lat": -3.78874, "lon": 102.25070, "icon": "monument", "color": "darkred"},
    {"name": "Pantai Panjang", "lat": -3.8118, "lon": 102.2660, "icon": "umbrella-beach", "color": "blue"},
    {"name": "Bandara Fatmawati Soekarno", "lat": -3.8631, "lon": 102.3106, "icon": "plane-departure", "color": "cadetblue"},
    {"name": "Universitas Bengkulu", "lat": -3.7667, "lon": 102.2667, "icon": "university", "color": "purple"},
    {"name": "Rumah Sakit M. Yunus", "lat": -3.7890, "lon": 102.2660, "icon": "hospital", "color": "red"},
    {"name": "Pusat Perbelanjaan Bencoolen Mall", "lat": -3.7909, "lon": 102.2610, "icon": "shopping-bag", "color": "cadetblue"},
    {"name": "Pasar Tradisional Panorama", "lat": -3.7975, "lon": 102.2605, "icon": "store", "color": "lightgray"},
    {"name": "Museum Negeri Bengkulu", "lat": -3.7942, "lon": 102.2615, "icon": "building", "color": "green"},
    {"name": "Kantor Gubernur Bengkulu", "lat": -3.7915, "lon": 102.2640, "icon": "landmark", "color": "darkred"},
    {"name": "Dinas Pendidikan Provinsi Bengkulu", "lat": -3.7920, "lon": 102.2630, "icon": "school", "color": "darkblue"},
    {"name": "Pengadilan Negeri Bengkulu", "lat": -3.7960, "lon": 102.2625, "icon": "balance-scale", "color": "gray"},
    {"name": "Kejaksaan Tinggi Bengkulu", "lat": -3.7962, "lon": 102.2620, "icon": "gavel", "color": "darkpurple"},
    {"name": "Kantor Walikota Bengkulu", "lat": -3.7930, "lon": 102.2650, "icon": "city", "color": "darkgreen"},
    {"name": "Terminal Betung", "lat": -3.8050, "lon": 102.2550, "icon": "bus", "color": "darkgreen"},
    {"name": "Stadion Semarak Sawah Lebar", "lat": -3.7750, "lon": 102.2750, "icon": "futbol", "color": "darkred"},
]

# Opsi untuk dropdown form
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEATHER_CONDITIONS = ["Cerah", "Berawan", "Hujan", "Hujan Lebat"]

# --- Helper Functions ---
def calculate_traffic_prediction(road_name, hour, day, weather):
    """Menghitung perkiraan volume lalu lintas berdasarkan input."""
    road_info = ROAD_DATA.get(road_name, {})
    capacity = road_info.get("capacity", 1000)
    
    base_volume = capacity * 0.6 

    # Pengaruh waktu puncak
    if 7 <= hour <= 9 or 16 <= hour <= 18:
        base_volume *= 1.3 
    elif 12 <= hour <= 14:
        base_volume *= 1.1 

    # Pengaruh hari kerja/libur
    if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        base_volume *= 1.1 
    elif day in ["Saturday"]:
        base_volume *= 1.05 

    # Pengaruh cuaca
    if weather == "Hujan":
        base_volume *= 1.15 
    elif weather == "Hujan Lebat":
        base_volume *= 1.3 

    predicted_vehicle_count = int(base_volume)
    percentage_capacity = (predicted_vehicle_count / capacity) * 100

    congestion_level, congestion_color = "Normal", "green"
    if percentage_capacity >= 100:
        congestion_level, congestion_color = "Macet", "red"
    elif percentage_capacity >= 80:
        congestion_level, congestion_color = "Sangat Padat", "red"
    elif percentage_capacity >= 60:
        congestion_level, congestion_color = "Padat", "orange"
    
    return predicted_vehicle_count, capacity, percentage_capacity, congestion_level, congestion_color

def create_folium_map(center_coords=[-3.792376, 102.260764], zoom_start=13):
    """Membuat objek peta Folium dasar."""
    return folium.Map(location=center_coords, zoom_start=zoom_start)

def add_important_locations_to_map(m, locations):
    """Menambahkan marker untuk lokasi-lokasi penting ke peta."""
    for loc in locations:
        folium.Marker(
            location=[loc["lat"], loc["lon"]],
            popup=f"<b>{loc['name']}</b>",
            icon=folium.Icon(color=loc.get("color", "darkgreen"), icon=loc.get("icon", "building"), prefix="fa")
        ).add_to(m)

def add_road_name_markers_to_map(m, traffic_data):
    """Menambahkan marker untuk nama jalan ke peta tanpa garis atau status kemacetan visual."""
    for road in traffic_data:
        if "lat" in road and "lon" in road:
            folium.Marker(
                location=[road["lat"], road["lon"]],
                popup=f"<b>Jalan: {road['road_name']}</b>",
                icon=folium.Icon(color="darkblue", icon="road", prefix="fa") # Ikon generik untuk jalan
            ).add_to(m)

# Fungsi untuk menambahkan rute alternatif di peta (TIDAK DIGUNAKAN LAGI UNTUK MENGGAMBAR GARIS/POINT)
# def add_alternative_route_to_map(m, coords, name):
#     """Menambahkan rute alternatif yang dipilih ke peta."""
#     folium.PolyLine(
#         locations=coords,
#         color="blue",
#         weight=5,
#         opacity=0.8,
#         popup=f"Rute Alternatif: {name}"
#     ).add_to(m)
#     folium.Marker(
#         location=coords[0],
#         popup=f"Awal Rute Alternatif: {name}",
#         icon=folium.Icon(color="darkblue", icon="play", prefix="fa")
#     ).add_to(m)
#     folium.Marker(
#         location=coords[-1],
#         popup=f"Akhir Rute Alternatif: {name}",
#         icon=folium.Icon(color="darkblue", icon="flag", prefix="fa")
#     ).add_to(m)

def add_custom_legend(m):
    """Menambahkan legenda kustom ke peta. Legenda ini mungkin tidak lagi sepenuhnya relevan jika garis dihapus."""
    legend_html = '''
           <div style="position: fixed; 
                       bottom: 50px; left: 50px; width: 120px; height: 100px; 
                       border:2px solid grey; z-index:9999; font-size:14px;
                       background-color:white; opacity:0.9; padding: 10px; border-radius: 8px;">
             <b>Keterangan:</b> <br>
             <i style="background:#28a745; width:18px; height:18px; border-radius:50%; display:inline-block;"></i> Lancar <br>
             <i style="background:#f39c12; width:18px; height:18px; border-radius:50%; display:inline-block;"></i> Padat <br>
             <i style="background:#e74c3c; width:18px; height:18px; border-radius:50%; display:inline-block;"></i> Macat
           </div>
           '''
    m.get_root().html.add_child(folium.Element(legend_html))

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_traffic = None
    current_time_wib = datetime.now()
    
    selected_alternative_route_coords = None 
    selected_alternative_route_name = None

    if request.method == 'POST':
        road_name = request.form['road_name']
        hour = int(request.form['hour'])
        day = request.form['day']
        weather = request.form['weather']
        
        selected_alt_route_index = request.form.get('selected_alt_route_index')

        # Hitung prediksi lalu lintas
        predicted_vehicle_count, capacity, percentage_capacity, congestion_level, congestion_color = \
            calculate_traffic_prediction(road_name, hour, day, weather)

        road_info = ROAD_DATA.get(road_name, {})
        alternative_routes_data = road_info.get("alternative_routes", [])

        alternative_routes_for_display = []
        for i, alt_route in enumerate(alternative_routes_data):
            alternative_routes_for_display.append({"name": alt_route["name"], "index": i})
        
        # Logika ini tetap ada untuk menampilkan rute alternatif di panel prediksi,
        # namun tidak lagi digunakan untuk menggambar di peta.
        if selected_alt_route_index:
            try:
                idx = int(selected_alt_route_index)
                if 0 <= idx < len(alternative_routes_data):
                    selected_alternative_route_coords = alternative_routes_data[idx]["path_coords"]
                    selected_alternative_route_name = alternative_routes_data[idx]["name"]
            except ValueError:
                pass 

        predicted_traffic = {
            "road_name": road_name,
            "predicted_vehicle_count": predicted_vehicle_count,
            "capacity": capacity,
            "percentage_capacity": percentage_capacity,
            "hour": hour,
            "day": day,
            "weather": weather,
            "congestion_level": congestion_level,
            "congestion_color": congestion_color,
            "alternative_routes": alternative_routes_for_display
        }

    # Inisialisasi peta Folium
    m = create_folium_map()

    # Tambahkan lokasi penting ke peta
    add_important_locations_to_map(m, IMPORTANT_LOCATIONS)

    # Tambahkan marker nama jalan ke peta (BUKAN GARIS LALU LINTAS)
    add_road_name_markers_to_map(m, CURRENT_TRAFFIC_DATA)
    
    # Bagian untuk menggambar rute alternatif di peta dihilangkan karena permintaan untuk menghapus garis dan poin.
    # if selected_alternative_route_coords:
    #     add_alternative_route_to_map(m, selected_alternative_route_coords, selected_alternative_route_name)

    # Legenda mungkin tidak lagi sepenuhnya relevan tanpa garis berwarna,
    # namun tetap disertakan jika Anda ingin mempertahankan struktur.
    add_custom_legend(m)

    map_html = m._repr_html_()

    return render_template(
        'index.html',
        current_date_time=current_time_wib.strftime("%A, %d %B %Y %H:%M"),
        now=current_time_wib,
        road_names=list(ROAD_DATA.keys()),
        days=DAYS_OF_WEEK,
        weather_conditions=WEATHER_CONDITIONS,
        predicted_traffic=predicted_traffic,
        current_traffic=CURRENT_TRAFFIC_DATA,
        map_html=map_html
    )

if __name__ == '__main__':
    app.run(debug=True)
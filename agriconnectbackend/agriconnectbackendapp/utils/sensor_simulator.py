import random
import time
import statistics
from datetime import datetime
import requests
from django.utils import timezone
from agriconnectbackendapp.models import Sensor, SensorData, Crop, FertilityRecord
from agriconnectbackendapp.utils.fertility import FertilityPredictor
from agriconnectbackendapp.utils.push import PushNotification


class SensorSimulator:
    WEATHER_API_KEY = "c966c146152d475794884615252210"
    WEATHER_URL = "http://api.weatherapi.com/v1/current.json"

    def __init__(self, random_seed=None):
        self.random_seed = random_seed
        if random_seed is not None:
            random.seed(random_seed)

        # Load all sensors
        self.sensors = Sensor.objects.all()
        # Initialize buffer for each sensor: {sensor_id: [data1, data2, ...]}
        self.buffers = {sensor.id: [] for sensor in self.sensors}

    def generate_sensor_data(self, sensor):
        """Generate 1-min simulated data for a sensor"""
        return {
            "timestamp": timezone.now(),
            "pH": round(random.uniform(5.5, 8.0), 1),
            "Light_Hours": random.randint(8, 14),
            "Light_Intensity": random.randint(200, 1000),
            "Rh": random.randint(40, 95),
            "Nitrogen": random.randint(50, 300),
            "Phosphorus": random.randint(40, 250),
            "Potassium": random.randint(50, 350),
            "Yield": random.randint(10, 50),
            "N_Ratio": random.randint(5, 20),
            "P_Ratio": random.randint(5, 20),
            "K_Ratio": random.randint(5, 20),
        }

    def get_weather(self, farm):
        """Fetch weather for a farm's coordinates"""
        if farm.latitude is None or farm.longitude is None:
            return {}
        q = f"{farm.latitude},{farm.longitude}"
        try:
            resp = requests.get(self.WEATHER_URL, params={
                "key": self.WEATHER_API_KEY,
                "q": q,
                "aqi": "no"
            }, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get("current", {})
                return {
                    "temp_c": data.get("temp_c"),
                    "humidity": data.get("humidity"),
                    "wind_kph": data.get("wind_kph"),
                    "precip_mm": data.get("precip_mm")
                }
        except Exception as e:
            print(f"Weather API error for farm {farm.id}: {e}")
        return {}

    def determine_season(self, date=None):
        """Return season based on month (Southern Hemisphere example)"""
        date = date or timezone.now().date()
        month = date.month
        if month in [12, 1, 2]:
            return "Summer"
        elif month in [3, 4, 5]:
            return "Autumn"
        elif month in [6, 7, 8]:
            return "Winter"
        else:
            return "Spring"

    def add_to_buffer(self, sensor, data):
        """Add data to buffer, process average after 15 readings"""
        buf = self.buffers[sensor.id]
        buf.append(data)
        if len(buf) >= 15:
            self.process_average(sensor, buf)
            self.buffers[sensor.id] = []

    def process_average(self, sensor, data_list):
        """Compute averages, fetch weather, save to DB, run fertility prediction"""
        numeric_fields = ["pH", "Light_Hours", "Light_Intensity",
                          "Rh", "Nitrogen", "Phosphorus", "Potassium",
                          "Yield", "N_Ratio", "P_Ratio", "K_Ratio"]

        avg_data = {k: round(statistics.mean([d[k] for d in data_list]), 2) for k in numeric_fields}
        first_record = data_list[0]

        crop = sensor.crop
        farm = sensor.farm

        weather = self.get_weather(farm)
        season = self.determine_season()

        # Save sensor data
        sensor_data_obj = SensorData.objects.create(
            sensor=sensor,
            plant_name=crop.name,
            photoperiod=crop.photoperiod,
            temperature=weather.get("temp_c"),
            rainfall=weather.get("precip_mm"),
            ph=avg_data["pH"],
            light_hours=avg_data["Light_Hours"],
            light_intensity=avg_data["Light_Intensity"],
            rh=avg_data["Rh"],
            nitrogen=avg_data["Nitrogen"],
            phosphorus=avg_data["Phosphorus"],
            potassium=avg_data["Potassium"],
            yield_value=avg_data["Yield"],
            category_ph=first_record.get("Category_pH", "neutral"),
            soil_type=first_record.get("Soil_Type", "Loam"),
            season=season,
            n_ratio=avg_data["N_Ratio"],
            p_ratio=avg_data["P_Ratio"],
            k_ratio=avg_data["K_Ratio"],
            recorded_at=timezone.now()
        )

        print(f"[{datetime.now()}] ✅ Saved 15-min average for {crop.name} (Sensor #{sensor.id})")
        if weather:
            print(f"🌤️ Weather data: {weather}")

        # Prepare data for fertility prediction
        sensor_data_dict = {
            "Name": crop.name,
            "Photoperiod": crop.photoperiod,
            "Temperature": sensor_data_obj.temperature,
            "Rainfall": sensor_data_obj.rainfall,
            "pH": sensor_data_obj.ph,
            "Light_Hours": sensor_data_obj.light_hours,
            "Light_Intensity": sensor_data_obj.light_intensity,
            "Rh": sensor_data_obj.rh,
            "Nitrogen": sensor_data_obj.nitrogen,
            "Phosphorus": sensor_data_obj.phosphorus,
            "Potassium": sensor_data_obj.potassium,
            "Yield": sensor_data_obj.yield_value,
            "Category_pH": sensor_data_obj.category_ph,
            "Soil_Type": sensor_data_obj.soil_type,
            "Season": sensor_data_obj.season,
            "N_Ratio": sensor_data_obj.n_ratio,
            "P_Ratio": sensor_data_obj.p_ratio,
            "K_Ratio": sensor_data_obj.k_ratio,
        }

        # Predict fertility
        predictor = FertilityPredictor(crop.id, sensor_data_dict)
        fertility, recommendations = predictor.predict()

        FertilityRecord.objects.create(
            sensor=sensor,
            sensor_data=sensor_data_obj,
            fertility_level=fertility,
            recommendations=recommendations
        )

        print(f"📦 Fertility record saved for {crop.name} (Sensor #{sensor.id})")
        print(f"Predicted fertility: {fertility}, Recommendations: {recommendations}")
        
        # Send push notification if fertility is not High
        if fertility != "High":
            message = f"⚠️ Fertility for {crop.name} is {fertility}! Check recommendations."
            PushNotification.send_push_notification(user_id=crop.farm.owner.id, message=message)
            print(f"📣 Notification sent: {message}")

    def run(self, interval_seconds=60):
        """Run simulation for all sensors continuously"""
        print("🌱 Starting simulation for all sensors...")
        while True:
            for sensor in self.sensors:
                data = self.generate_sensor_data(sensor)
                print(f"[{data['timestamp']}] Sensor #{sensor.id} reading for {sensor.crop.name}: {data}")
                self.add_to_buffer(sensor, data)
            time.sleep(interval_seconds)

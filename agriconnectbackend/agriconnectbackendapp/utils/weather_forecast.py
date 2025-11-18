import time
import requests
from datetime import datetime
from django.utils import timezone
from agriconnectbackendapp.models import Farm, WeatherAlert
from agriconnectbackendapp.utils.weather_thresholds import WEATHER_THRESHOLDS
from agriconnectbackendapp.utils.push import PushNotification

class WeatherForecastJob:

    WEATHER_API_KEY = "c966c146152d475794884615252210"
    WEATHER_URL = "http://api.weatherapi.com/v1/forecast.json"

    def run(self, interval_seconds=3600):  
        print("🌦️ Starting hourly weather monitoring job...")

        while True:
            farms = Farm.objects.all()
            current_hour = datetime.now().hour
            hour_to_check = (current_hour + 1) % 24  

            for farm in farms:
                if farm.latitude is None or farm.longitude is None:
                    continue

                q = f"{farm.latitude},{farm.longitude}"

                try:
                    resp = requests.get(self.WEATHER_URL, params={
                        "key": self.WEATHER_API_KEY,
                        "q": q,
                        "aqi": "no",
                        "days": 1,
                        "hour": hour_to_check
                    }, timeout=10)

                    if resp.status_code != 200:
                        print(f"❌ Weather API error for farm {farm.id}: Status {resp.status_code}")
                        continue

                    data = resp.json()
                    hourly_forecast = data["forecast"]["forecastday"][0]["hour"]
                    
                    
                    first_hour = hourly_forecast[0]
                   
                    code = first_hour["condition"]["code"]
                  
                    print(code)
                    severity = None
                    if code in WEATHER_THRESHOLDS["EXTREME"]:
                        severity = "EXTREME"
                    elif code in WEATHER_THRESHOLDS["HIGH"]:
                        severity = "HIGH"

                    if severity:
                        details = WEATHER_THRESHOLDS[severity][code]

                        WeatherAlert.objects.create(
                            farm=farm,
                            severity=severity,
                            weather_code=code,
                            alert_title=details["alert"],
                            recommendation=details["recommendation"]
                        )

                    
                        PushNotification.send_push_notification(
                            user_id=farm.owner.id,
                            message=details["recommendation"]
                        )

                        print(f"✅ Alert sent for farm {farm.name} ({severity}): {details['alert']}")

                except Exception as e:
                    print(f"❌ Weather API Error for farm {farm.id}: {e}")

            print(f"⏳ Sleeping for {interval_seconds} seconds until next check...")
            time.sleep(interval_seconds)

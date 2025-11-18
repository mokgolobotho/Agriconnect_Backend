from django.core.management.base import BaseCommand
from agriconnectbackendapp.utils.weather_forecast import WeatherForecastJob

class Command(BaseCommand):
    help = "run weather forecast continuously."

    def handle(self, *args, **kwargs):
        WeatherForecastJob().run()
        self.stdout.write(self.style.SUCCESS("Hourly weather forecast job executed."))
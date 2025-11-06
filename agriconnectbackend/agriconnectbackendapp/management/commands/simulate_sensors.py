from django.core.management.base import BaseCommand
from agriconnectbackendapp.utils.sensor_simulator import SensorSimulator

class Command(BaseCommand):
    help = "Simulate all sensors continuously."

    def handle(self, *args, **options):
        simulator = SensorSimulator(random_seed=42)
        simulator.run()

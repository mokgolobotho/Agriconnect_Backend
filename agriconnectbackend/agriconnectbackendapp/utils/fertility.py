# agriconnectbackendapp/utils/fertility_predictor.py
from agriconnectbackendapp.models import Crop
from agriconnectbackendapp.ml_model.model import predict_fertility, predict_name
from agriconnectbackendapp.ml_model.recommendations import generate_recommendations

class FertilityPredictor:
    def __init__(self, crop_id, sensor_data):
        """
        crop_id: ID of the Crop object
        sensor_data: dict of sensor readings (Temperature, Rainfall, pH, etc.)
        """
        self.crop_id = crop_id
        self.sensor_data = sensor_data
        self.crop = None
        self._load_crop()

    def _load_crop(self):
        try:
            self.crop = Crop.objects.get(pk=self.crop_id)
        except Crop.DoesNotExist:
            raise ValueError(f"Crop with id {self.crop_id} does not exist")

    def predict(self):
        """Return predicted fertility and recommendations"""
        # Prepend crop name to sensor_data
        sensor_data_with_name = {"Name": self.crop.name, **self.sensor_data}

        fertility = predict_fertility(sensor_data_with_name)
        recommendations = generate_recommendations(sensor_data_with_name) if fertility != "High" else []

        return fertility, recommendations


optimal_ranges = {
    "Nitrogen": (200, 300),
    "Phosphorus": (120, 200),
    "Potassium": (250, 350),
    "pH": (6.5, 7.5),
    "Temperature": (20, 25),
    "Rainfall": (600, 800),
    "Light_Hours": (10, 14),
    "Rh": (50, 80),
}

def generate_recommendations(sensor_data):
    recommendations = []

    for param, (low, high) in optimal_ranges.items():
        value = sensor_data.get(param)
        if value is None:
            continue
        if value < low:
            recommendations.append(f"Increase {param} (currently {value}, optimal {low}-{high})")
        elif value > high:
            recommendations.append(f"Reduce {param} (currently {value}, optimal {low}-{high})")

    return recommendations

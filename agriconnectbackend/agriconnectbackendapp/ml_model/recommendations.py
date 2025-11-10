def generate_recommendations(sensor_data):
    recommendations = []

    # --- Generic Optimal Ranges ---
    optimal_ranges = {
        "Nitrogen": (200, 300),
        "Phosphorus": (120, 200),
        "Potassium": (250, 350),
        "pH": (6.0, 7.5),
        "Temperature": (20, 30),
        "Rainfall": (600, 800),
        "Light_Hours": (8, 14),
        "Rh": (50, 80),
        "Light_Intensity": (400, 900)
    }

    # --- Check generic parameters ---
    for param, (low, high) in optimal_ranges.items():
        value = sensor_data.get(param)
        if value is None:
            continue

        if value < low:
            if param in ["Nitrogen", "Phosphorus", "Potassium"]:
                recommendations.append(
                    f"Increase {param} (currently {value}, optimal {low}-{high}). "
                    f"Consider applying a balanced fertilizer such as NPK 20-20-20."
                )
            elif param == "pH":
                recommendations.append(
                    f"Increase soil pH (currently {value}, optimal {low}-{high}). "
                    f"Apply agricultural lime or dolomite."
                )
            elif param == "Temperature":
                recommendations.append(
                    f"Temperature is too low ({value}°C). Consider using mulch or temporary covers to retain warmth."
                )
            elif param == "Rainfall":
                recommendations.append(
                    f"Low rainfall detected ({value} mm). Please irrigate your crops to maintain soil moisture."
                )
            elif param == "Light_Hours":
                recommendations.append(
                    f"Insufficient light ({value} hours). Move plants to a sunnier area if possible."
                )
            elif param == "Light_Intensity":
                recommendations.append(
                    f"Light intensity is low ({value}). Consider cleaning dust off leaves or adjusting shade nets."
                )
        elif value > high:
            if param in ["Nitrogen", "Phosphorus", "Potassium"]:
                recommendations.append(
                    f"Reduce {param} levels (currently {value}, optimal {low}-{high}). "
                    f"Over-fertilization can damage plants."
                )
            elif param == "pH":
                recommendations.append(
                    f"Soil pH is too high ({value}). Apply elemental sulfur or organic compost to reduce pH."
                )
            elif param == "Temperature":
                recommendations.append(
                    f"Temperature is too high ({value}°C). Use shade nets or water more frequently to cool the plants."
                )
            elif param == "Rainfall":
                recommendations.append(
                    f"Too much rainfall ({value} mm). Ensure good drainage to avoid waterlogging."
                )
            elif param == "Light_Hours":
                recommendations.append(
                    f"Too much light exposure ({value} hours). Consider building a light shade for your plants."
                )
            elif param == "Light_Intensity":
                recommendations.append(
                    f"Excessive light intensity ({value}). Use shade nets to protect crops from sunburn."
                )

    # --- Coupled Temperature & Rainfall Logic ---
    temp = sensor_data.get("Temperature")
    rain = sensor_data.get("Rainfall")

    if temp and rain:
        if temp > 30 and rain < 600:
            recommendations.append(
                "High temperature with low rainfall detected — increase irrigation frequency."
            )
        elif temp < 20 and rain > 800:
            recommendations.append(
                "Cool and wet conditions detected — ensure proper drainage and reduce watering."
            )

    # --- Combine final message ---
    if not recommendations:
        recommendations.append("All parameters are within optimal ranges. Keep up the good work!")

    return recommendations

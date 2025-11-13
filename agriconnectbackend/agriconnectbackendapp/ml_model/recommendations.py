def generate_recommendations(sensor_data):
    recommendations = []

    # --- Generic Optimal Ranges ---
    optimal_ranges = {
        "Nitrogen": (200, 300),
        "Phosphorus": (120, 200),
        "Potassium": (250, 350),
        "pH": (6.0, 7.5),
        "Temperature": (20, 30),  # °C
        "Rainfall": (600, 800),   # mm
        "Light_Hours": (8, 14),
        "Rh": (50, 80),
        "Light_Intensity": (400, 900)
    }

    # --- Check individual parameters ---
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
                    f"Increase soil pH (currently {value}, optimal {low}-{high}). Apply lime or dolomite."
                )
            elif param == "Temperature":
                recommendations.append(
                    f"Temperature is low ({value}°C). Use mulch or covers to retain warmth."
                )
            elif param == "Rainfall":
                recommendations.append(
                    f"Low rainfall detected ({value} mm). Please irrigate your crops to maintain soil moisture."
                )
            elif param == "Light_Hours":
                recommendations.append(
                    f"Insufficient light ({value} hours). Move plants to sunnier spots."
                )
            elif param == "Light_Intensity":
                recommendations.append(
                    f"Light intensity is low ({value}). Adjust shade or clean leaves."
                )
        elif value > high:
            if param in ["Nitrogen", "Phosphorus", "Potassium"]:
                recommendations.append(
                    f"Reduce {param} levels (currently {value}, optimal {low}-{high}). Over-fertilization can damage plants."
                )
            elif param == "pH":
                recommendations.append(
                    f"Soil pH is high ({value}). Apply sulfur or compost to reduce pH."
                )
            elif param == "Temperature":
                recommendations.append(
                    f"Temperature is high ({value}°C). Use shade nets or water more frequently."
                )
            elif param == "Rainfall":
                recommendations.append(
                    f"Excessive rainfall ({value} mm). Ensure proper drainage."
                )
            elif param == "Light_Hours":
                recommendations.append(
                    f"Too much light ({value} hours). Provide shade if necessary."
                )
            elif param == "Light_Intensity":
                recommendations.append(
                    f"Excessive light intensity ({value}). Use shade nets to protect crops."
                )

    # --- Coupled Temperature & Rainfall Logic ---
    temp = sensor_data.get("Temperature")
    rain = sensor_data.get("Rainfall")

    if temp is not None and rain is not None:
        if temp > 30 and rain < 600:
            recommendations.append(
                "⚠️ High temperature with low rainfall — irrigation is recommended."
            )
        elif temp < 20 and rain > 800:
            recommendations.append(
                "⚠️ Cool and wet conditions — avoid overwatering and ensure proper drainage."
            )

    if not recommendations:
        recommendations.append("All parameters are within optimal ranges. Keep up the good work!")

    return recommendations

def generate_recommendations(sensor_data):
    recommendations = []

    # --- Generic Optimal Ranges ---
    optimal_ranges = {
        "Nitrogen": (200, 300),
        "Phosphorus": (120, 200),
        "Potassium": (250, 350),
        "pH": (6.0, 7.5),
        "Temperature": (20, 30),      # Air temperature in °C
        "Rainfall": (600, 800),       # mm
        "Rh": (50, 80),               # Relative Humidity %
        "Light_Hours": (8, 14),       # Hours
        "Light_Intensity": (400, 900) # Lux
    }

    # --- Check N, P, K individually ---
    for nutrient in ["Nitrogen", "Phosphorus", "Potassium"]:
        value = sensor_data.get(nutrient)
        if value is None:
            continue
        low, high = optimal_ranges[nutrient]
        if value < low:
            recommendations.append(
                f"Increase {nutrient} (currently {value}, optimal {low}-{high}). "
                f"Consider applying a balanced fertilizer such as NPK 20-20-20."
            )
        elif value > high:
            recommendations.append(
                f"Reduce {nutrient} levels (currently {value}, optimal {low}-{high}). Over-fertilization can damage plants."
            )

    # --- Check pH ---
    ph = sensor_data.get("pH")
    if ph is not None:
        low, high = optimal_ranges["pH"]
        if ph < low:
            recommendations.append(
                f"Increase soil pH (currently {ph}, optimal {low}-{high}). Apply lime or dolomite."
            )
        elif ph > high:
            recommendations.append(
                f"Soil pH is high ({ph}). Apply sulfur or compost to reduce pH."
            )

    # --- Check Light Hours and Light Intensity ---
    for light_param in ["Light_Hours", "Light_Intensity"]:
        value = sensor_data.get(light_param)
        if value is None:
            continue
        low, high = optimal_ranges[light_param]
        if value < low:
            msg = (
                f"Insufficient {light_param.replace('_', ' ')} ({value}). "
                f"{'Move plants to sunnier spots.' if light_param == 'Light_Hours' else 'Adjust shade or clean leaves.'}"
            )
            recommendations.append(msg)
        elif value > high:
            msg = (
                f"Too much {light_param.replace('_', ' ')} ({value}). "
                f"{'Provide shade if necessary.' if light_param == 'Light_Hours' else 'Use shade nets to protect crops.'}"
            )
            recommendations.append(msg)

    # --- Combined Air Temperature, Rainfall, and RH Logic ---
    temp = sensor_data.get("Temperature")
    rain = sensor_data.get("Rainfall")
    rh = sensor_data.get("Rh")

    if temp is not None and rain is not None and rh is not None:
        low_temp, high_temp = optimal_ranges["Temperature"]
        low_rain, high_rain = optimal_ranges["Rainfall"]
        low_rh, high_rh = optimal_ranges["Rh"]

        if temp > high_temp and rain < low_rain and rh < low_rh:
            recommendations.append(
                "⚠️ High air temperature with low rainfall and low humidity — irrigation is strongly recommended."
            )
        elif temp < low_temp and rain > high_rain and rh > high_rh:
            recommendations.append(
                "⚠️ Cool, wet, and humid conditions — avoid overwatering and ensure proper drainage."
            )
        elif temp > high_temp:
            recommendations.append(
                f"Air temperature is high ({temp}°C). Use shade nets or water more frequently."
            )
        elif temp < low_temp:
            recommendations.append(
                f"Air temperature is low ({temp}°C). Use mulch or covers to retain warmth."
            )
        if rain < low_rain:
            recommendations.append(
                f"Low rainfall detected ({rain} mm). Please irrigate your crops to maintain soil moisture."
            )
        elif rain > high_rain:
            recommendations.append(
                f"Excessive rainfall ({rain} mm). Ensure proper drainage."
            )
        if rh < low_rh:
            recommendations.append(
                f"Relative Humidity is low ({rh}%). Consider misting or increasing humidity."
            )
        elif rh > high_rh:
            recommendations.append(
                f"Relative Humidity is high ({rh}%). Ensure proper airflow to prevent fungal diseases."
            )

    # --- Fallback ---
    if not recommendations:
        recommendations.append("All parameters are within optimal ranges. Keep up the good work!")

    return recommendations

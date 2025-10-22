import joblib
import pandas as pd
import os

# Get the directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load all saved model assets
model = joblib.load(os.path.join(BASE_DIR, "fertility_model.pkl"))
label_encoders = joblib.load(os.path.join(BASE_DIR, "fertility_label_encoders.pkl"))
target_encoder = joblib.load(os.path.join(BASE_DIR, "fertility_target_encoder.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "fertility_features.pkl"))


def predict_fertility(data):
    """
    Predicts fertility category based on input features including crop name.
    Returns a readable fertility label (e.g., 'Low', 'Moderate', 'High').
    """
    try:
        # ✅ Convert incoming data to DataFrame
        df = pd.DataFrame([data])

        # ✅ Ensure all required features exist
        for col in features:
            if col not in df.columns:
                df[col] = 0

        # ✅ Encode categorical columns
        for col, encoder in label_encoders.items():
            if col in df.columns:
                try:
                    df[col] = encoder.transform(df[col])
                except ValueError:
                    # Handle unseen category
                    df[col] = [-1 for _ in range(len(df))]

        # ✅ Reorder columns to match training feature order
        df = df[features]

        # ✅ Predict encoded class
        pred_encoded = model.predict(df)[0]

        # ✅ Decode numeric label back to text (e.g., 'Moderate')
        try:
            pred_label = target_encoder.inverse_transform([int(pred_encoded)])[0]
        except Exception:
            pred_label = str(pred_encoded)

        return pred_label

    except Exception as e:
        print(f"⚠️ Fertility prediction error: {e}")
        return "Unknown"

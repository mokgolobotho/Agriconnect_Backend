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

model2 = joblib.load(os.path.join(BASE_DIR, "photoperiod_model_name_only.pkl"))
name_encoder2 = joblib.load(os.path.join(BASE_DIR, "name_encoder.pkl"))
target_encoder2 = joblib.load(os.path.join(BASE_DIR, "photoperiod_target_encoder.pkl"))

def predict_fertility(data):

    try:
        df = pd.DataFrame([data])

        for col in features:
            if col not in df.columns:
                df[col] = 0

        for col, encoder in label_encoders.items():
            if col in df.columns:
                try:
                    df[col] = encoder.transform(df[col])
                except ValueError:
                    df[col] = [-1 for _ in range(len(df))]

        df = df[features]

        pred_encoded = model.predict(df)[0]

        try:
            pred_label = target_encoder.inverse_transform([int(pred_encoded)])[0]
        except Exception:
            pred_label = str(pred_encoded)

        return pred_label

    except Exception as e:
        print(f"⚠️ Fertility prediction error: {e}")
        return "Short Day Period"

def predict_name(name):
    try:
        name = name.lower()
        name_encoded = name_encoder2.transform([name]).reshape(-1, 1)

        pred = model2.predict(name_encoded)
        photoperiod = target_encoder2.inverse_transform(pred)[0]
        return photoperiod
    except Exception as e:
        print(f"⚠️ Photoperiod prediction error: {e}")
        return "Unknown"

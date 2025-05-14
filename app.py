
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

model = joblib.load("crop_yield_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        rainfall = float(data["rainfall"])
        pesticides = float(data["pesticides"])
        temperature = float(data["temperature"])

        input_df = pd.DataFrame({
            "Country_Encoded": [0],
            "Item_Encoded": [0],
            "Pesticides": [pesticides],
            "Avg_Temp": [temperature],
            "Rainfall": [rainfall]
        })

        prediction = model.predict(input_df)
        return jsonify({"predicted_yield": round(float(prediction[0]), 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/batch-predict", methods=["POST"])
def batch_predict():
    if 'file' not in request.files:
        return jsonify({"error": "CSV file is required"}), 400

    file = request.files['file']
    try:
        df = pd.read_csv(file)
        required_columns = ["Year", "average_rain_fall_mm_per_year", "pesticides_tonnes", "avg_temp"]
        if not all(col in df.columns for col in required_columns):
            return jsonify({"error": f"CSV must contain columns: {', '.join(required_columns)}"}), 400

        df = df.rename(columns={
            "average_rain_fall_mm_per_year": "Rainfall",
            "pesticides_tonnes": "Pesticides",
            "avg_temp": "Avg_Temp"
        })
        df["Country_Encoded"] = 0
        df["Item_Encoded"] = 0

        feature_order = ["Country_Encoded", "Item_Encoded", "Pesticides", "Avg_Temp", "Rainfall"]
        prediction = model.predict(df[feature_order])
        df["Predicted_Yield"] = prediction

        result = df.to_dict(orient="records")
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

import asyncio
from flask import Flask, jsonify
import joblib
import pandas as pd
from collections import deque
from threading import Lock
import myo
import time

app = Flask(__name__)

class EmgPredictor(myo.DeviceListener):
    def __init__(self, model_path):
        self.model_path = model_path
        self.lock = Lock()
        self.emg_data = deque(maxlen=500)  # Collecting 100 EMG data points every 5 seconds
        self.model = self.load_model(self.model_path)
        self.prediction = None
        self.timer = 0
        self.interval = 4  # 4 seconds
        self.start_time = time.time()

        # Movement labels
        self.label_mapping = {
            "1": 1,  
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
        }

    def load_model(self, model_path):
        return joblib.load(model_path)

    def predict_emg(self):
        with self.lock:
            emg_df = pd.DataFrame(self.emg_data)
            if not emg_df.empty:
                sensor_data = emg_df.iloc[:, :8]  # Only sensor values
                self.prediction = self.model.predict(sensor_data)

    def on_connected(self, event):
        print("Myo connected...")
        event.device.stream_emg(True)
        self.start_time = time.time()

    def on_disconnected(self, event):
        print("Myo disconnected...")

    def on_emg(self, event):
        self.get_emg_data(event.emg)
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.interval:
            self.start_time = time.time()
            self.predict_emg()

    def get_emg_data(self, emg):
        with self.lock:
            self.emg_data.append(emg)

    def map_label(self, label):
        for move, move_label in self.label_mapping.items():
            if label == move_label:
                return move
        return "Unknown"

predictor = EmgPredictor(model_path="C:/Users/Eda ÇETİN/Downloads/egitilen_model_boosting (2).pkl")

@app.route('/get_sayi', methods=['GET'])
async def get_prediction():
    if predictor.prediction is not None:
        mapped_label = predictor.map_label(predictor.prediction[0])
        return jsonify({"prediction": mapped_label})
        await asyncio.sleep(4)
        return response
    else:
        return jsonify({"message": "No prediction available yet."})

if __name__ == '__main__':
    myo.init(sdk_path="C:/myo-sdk-win-0.9.0")
    hub = myo.Hub()
    with hub.run_in_background(predictor.on_event):
        app.run(debug=True) 
# EMG Hand Movement Prediction with Myo Armband and Flask

This project provides a real-time hand movement prediction system using the Myo Armband and a pre-trained machine learning model. The application streams EMG data from the Myo Armband, processes it using a machine learning model (Boosting), and serves predictions through a Flask API.

## Overview

This system uses the Myo Armband to collect electromyography (EMG) signals and makes real-time predictions of hand movements using a machine learning model. The predictions are exposed via a Flask-based API.

The EMG data is captured from the Myo device at an interval of 4 seconds, passed through a trained Boosting model, and the predicted movement label is returned via the `/get_sayi` endpoint.
## Requirements

- Python 3.x
- Flask
- Myo SDK (version 0.9.0)
- Joblib (for loading the pre-trained model)
- Pandas
- Scikit-learn

## Hardware Requirements:
* **Myo Armband:** Used for capturing EMG signals.
* **Myo SDK:** Myo software development kit for integrating the armband.

from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db
import numpy as np
import tensorflow as tf
import joblib

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("flask_file/key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://soil-sensor-aa433-default-rtdb.firebaseio.com'
})

with open('converted_model.tflite', 'rb') as f:
    tflite_model = f.read()

# Memuat StandardScaler dan LabelEncoder yang telah disimpan
scaler = joblib.load('scaler.joblib')
label_encoder = joblib.load('label_encoder.joblib')

# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_content=tflite_model)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Membuat aplikasi Flask
app = Flask(__name__)

# Variabel global untuk hum_val dan ph_val
N_val = 0
P_val = 0
K_val = 0
hum_val = 0.0
ph_val = 0.0
temp_val = 0.0


# Fungsi untuk mendapatkan semua data dari Firebase
def get_all_data():
    global N_val, P_val, K_val, hum_val, ph_val, temp_val
    N = db.reference('/soil/N')
    P = db.reference('/soil/P')
    K = db.reference('/soil/K')
    hum = db.reference('/soil/hum')
    ph = db.reference('/soil/ph')
    temp = db.reference('/soil/temp')
    
    N_val = int(N.get())
    P_val = int(P.get())
    K_val = int(K.get())
    hum_val = round(float(hum.get()),2)
    ph_val = round(float(ph.get()),2)
    temp_val = round(float(temp.get()),2)

# Function to perform inference with TensorFlow Lite model
def perform_inference(input_data):
    input_data_scaled = scaler.transform(input_data).astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data_scaled)

    interpreter.invoke() #predict

    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

# Rute untuk halaman utama
@app.route('/')
def home():
    return render_template('index.html')

# Rute untuk mendapatkan semua data dari Firebase
@app.route('/data')
def get_data():
    global pred_params, predicted_label, crop_prediction

    get_all_data()
    
    pred_params = [N_val, P_val, K_val, temp_val, hum_val, ph_val]
    input_data = np.array([pred_params])

    # Perform inference dengan model TFLite
    prediction = perform_inference(input_data)

    # Ambil indeks label dengan nilai prediksi tertinggi
    predicted_label = label_encoder.inverse_transform(np.argmax(prediction, axis=1))
    crop_prediction = predicted_label[0]

    print(f'N: {N_val}')
    print(f'P: {P_val}')
    print(f'K: {K_val}')
    print(f'Humidity: {hum_val}')
    print(f'ph: {ph_val}')
    print(f'temp: {temp_val}')
    print(f"Tanaman yang direkomendasikan berdasarkan parameter yang dimasukkan adalah: {crop_prediction}")

    return jsonify(N_val, P_val, K_val, hum_val, ph_val, temp_val, crop_prediction)

if __name__ == '__main__':
    # Menjalankan aplikasi Flask
    app.run(debug=True)


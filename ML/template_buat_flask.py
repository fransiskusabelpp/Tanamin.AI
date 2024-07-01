from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf

# Initialize Flask app
app = Flask(__name__)

# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="crop_recommendation_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Function to perform inference with TensorFlow Lite model
def perform_inference(input_data):
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

# Map index label hasil prediksi ke nama tanaman
labels = ["label1", "label2", ..., "label22"]  # Ganti dengan nama label sesuai dataset Anda

# Endpoint untuk melakukan prediksi crop recommendation
@app.route("/predict-crop", methods=["POST"])
def predict_crop():
    try:
        # Ambil data dari permintaan
        data = request.json
        # Pastikan format data sesuai dengan model
        input_data = np.array(data['features'], dtype=np.float32)
        # Perform inference dengan model TFLite
        prediction = perform_inference(input_data)
        # Ambil indeks label dengan nilai prediksi tertinggi
        predicted_label_index = np.argmax(prediction)
        # Ambil nama tanaman dari label yang sesuai
        crop_recommendation = labels[predicted_label_index]
        return jsonify({"crop_recommendation": crop_recommendation}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

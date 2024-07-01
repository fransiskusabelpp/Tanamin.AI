import numpy as np
import tensorflow as tf

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="converted_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensor details.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

N = 21
P = 22
K = 25
temp = 30
hum = 40
ph = 6

#Input parameter untuk prediksi
pred_params = [N, P, K, temp, hum, ph]

# Prepare input data as numpy array (example values for N, P, K, pH, Kelembaban)
input_data = np.array([pred_params], dtype=np.float32)  # Adjust the input data accordingly

# Check input details to match the input shape
input_shape = input_details[0]['shape']

# Set the tensor for the input data
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run the model
interpreter.invoke()

# Get the prediction results
output_data = interpreter.get_tensor(output_details[0]['index'])

# Assuming the model returns a one-hot encoded output, you might need to decode it.
# For example, if your model output is a one-hot vector for 5 possible crops:
crop_names =  ['apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton', 'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans', 'mungbean', 'muskmelon', 'orange', 'papaya', 'pigeonpeas', 'pomegranate', 'rice', 'watermelon']  # Replace with actual crop names
predicted_crop_index = np.argmax(output_data)
predicted_crop = crop_names[predicted_crop_index]

print(f"Predicted crop: {predicted_crop}")

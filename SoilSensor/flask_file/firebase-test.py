

# import pyrebase

# # // Your web app's Firebase configuration
# config = {
#   "apiKey": "AIzaSyCC9IiRzPsvUls36Hk7CqfLnmh_qabsNrI",
#   "authDomain": "soil-sensor-aa433.firebaseapp.com",
#   "databaseURL": "https://soil-sensor-aa433-default-rtdb.firebaseio.com",
#   "projectId": "soil-sensor-aa433",
#   "storageBucket": "soil-sensor-aa433.appspot.com",
#   "messagingSenderId": "865389621603",
#   "appId": "1:865389621603:web:8c8a15f7c4ddae8e70a356"
# }

# firebase = pyrebase.initialize_app(config)

# db = firebase.database()



# # Get a database reference
# ref = db.reference('/')

# # Read data from the database
# data = ref.get()
# print(data)

# # Write data to the database
# ref.update({'new_data': 'value'})

# # Listen for changes in the database
# def listener(event):
#     print(event.event_type)  # can be 'put' or 'patch'
#     print(event.path)  # relative to the reference, no leading slash
#     print(event.data)

# ref.listen(listener)

# Route to get data from Firebase
# Membuat aplikasi Flask
# Membuat aplikasi Flask
# Membuat aplikasi Flask



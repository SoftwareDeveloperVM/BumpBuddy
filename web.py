from flask import Flask, request, jsonify, render_template_string


app = Flask(__name__)


latest_state = {
   "movement_state": "Crashed",
   "distance": None,
   "magnitude": None
}


HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Sensor Status</title>
   <meta http-equiv="refresh" content="1">
   <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
   <style>
       body {
           font-family: 'Roboto', sans-serif;
           background-color: #f4f4f9;
           margin: 0;
           padding: 0;
           display: flex;
           flex-direction: column;
           align-items: center;
           justify-content: center;
           min-height: 100vh;
       }


       h1 {
           color: #333;
           font-size: 2.5em;
           margin-bottom: 20px;
           text-align: center;
       }


       .state-container {
           background-color: #fff;
           padding: 30px;
           border-radius: 12px;
           box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
           width: 80%;
           max-width: 500px;
           text-align: center;
       }


       .state-container p {
           font-size: 1.2em;
           margin: 15px 0;
       }


       .state {
           font-size: 2em;
           font-weight: bold;
       }


       .distance, .magnitude {
           font-size: 1.5em;
           color: #777;
       }


       .state.crashed {
           color: #f44336;
       }


       .state.moving {
           color: #ff9800;
       }


       .state.rest {
           color: #4caf50;
       }


       .icon {
           font-size: 50px;
           margin: 20px 0;
       }


       .icon.crashed {
           color: #f44336;
       }


       .icon.moving {
           color: #ff9800;
       }


       .icon.rest {
           color: #4caf50;
       }


       @media (max-width: 600px) {
           .state-container {
               padding: 20px;
           }
           h1 {
               font-size: 2em;
           }
           .state, .distance, .magnitude {
               font-size: 1.2em;
           }
       }


   </style>
</head>
<body>


   <h1>Live Sensor Status</h1>


   <div class="state-container">
       <div class="icon {{ movement_state.lower() }}">
           {% if movement_state == 'Crashed' %}
               CRASH
           {% elif movement_state == 'Moving' %}
               MOVING
           {% elif movement_state == 'At Rest' %}
               AT REST
           {% endif %}
       </div>


       <p class="state {{ movement_state.lower() }}">{{ movement_state }}</p>
       <p class="distance">Distance: {{ distance }} cm</p>
       <p class="magnitude">Acceleration Magnitude: {{ magnitude }}</p>
   </div>


</body>
</html>
"""




@app.route('/')
def index():


   return render_template_string(
       HTML_TEMPLATE,
       movement_state=latest_state.get("movement_state", "Crashed"),
       distance=latest_state.get("distance", "N/A"),
       magnitude=latest_state.get("magnitude", "N/A")
   )


@app.route('/data', methods=['POST'])
def receive_data():
   try:
       data = request.get_json()
       if data is None:
           return jsonify({"error": "No JSON data received"}), 400


       latest_state["movement_state"] = data.get("movement_state", "Crashed")
       latest_state["distance"] = round(data.get("distance", 0.0), 4)
       latest_state["magnitude"] = round(data.get("magnitude", 0.0), 4)


       print("Data received:", latest_state)
       return jsonify({"message": "Data received successfully"}), 200
   except Exception as e:
       return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
   print("Sensor Server Running at http://localhost:5000")
   print("Use POST /data to submit sensor readings.")
   app.run(host='0.0.0.0', port=5000)

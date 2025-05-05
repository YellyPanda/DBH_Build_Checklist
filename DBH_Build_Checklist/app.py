from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Define the path for the JSON file in the user's Documents folder
user_home = os.path.expanduser("~")
SAVE_FILE = os.path.join(user_home, "Documents", "part_selection_state.json")

# Cars as of 05/03/2025
car_parts = {
    "IFA": {
        "Engine Parts": ["Engine - 10L Diesel", "Radiator - 24L", "Battery - 180A"],
        "Exterior Parts": ["Windshield", "Corner Window Right", "Corner Window Left", "Front Bumper",
                           "License Plate Front", "License Plate Back", "Battery Cover", "Roof Hatch", "Grille",
                           "Left Front Door", "Left Mirror", "Right Mirror", "Right Front Door", "Rear Window", "Cargo Bed"],
        "Interior Parts": ["Radio", "Glovebox Lid", "Engine Cover", "Dashboard", "Left Front Door Panel", "Right Front Door Panel",
                           "Steering Wheel", "Handbrake", "Shifter", "Floor Mat Driver", "Floor Mat Passenger",
                           "Seat Driver", "Seat Passenger", "Gas Pedal", "Brake Pedal", "Clutch Pedal"],
        "Wheel Parts": ["Wheel x4", "Tire x4"],
        "Lights": ["Headlight Left", "Headlight Right", "Front Left Side Turn Signal", "Front Right Side Turn Signal",
                   "Left Brake Light", "Right Brake Light", "Interior Dome Light Front", "Interior Dome Light Back"]
    }
}

# Load saved selection states
def load_saved_states():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}  # Ensure it returns a dictionary

# Save selection states
def save_states(states):
    with open(SAVE_FILE, "w") as f:
        json.dump(states, f, indent=4)

@app.route("/")
def home():
    selected_car = next(iter(car_parts))  # Default car model
    states = load_saved_states()
    return render_template("index.html", car_parts=car_parts, selected_car=selected_car, states=states)

@app.route("/get_parts/<car_model>")
def get_parts(car_model):
    return jsonify(car_parts.get(car_model, {}))  # Avoid returning Undefined

@app.route("/get_state/<car_model>")
def get_state(car_model):
    states = load_saved_states()
    return jsonify(states.get(car_model, {}))  # Ensure default value

@app.route("/save_state", methods=["POST"])
def save_state():
    data = request.json or {}  # Prevent NoneType errors
    save_states(data)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
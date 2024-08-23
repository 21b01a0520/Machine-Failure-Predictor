from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.pkl')

# Define failure types and parameter suggestions
failure_types = {
    0: "No Failure",
    1: "Tool Wear Failure",
    2: "Heat Dissipation Failure",
    3: "Power Failure",
    4: "Overstrain Failure"
}

parameter_suggestions = {
    1: "Reduce the tool wear by changing the tool more frequently.",
    2: "Ensure proper cooling to maintain a lower process temperature.",
    3: "Check and stabilize the power supply.",
    4: "Avoid overloading the machine by operating within recommended torque and speed limits."
}

# Detailed analysis for each failure type
detailed_analysis = {
    "Tool Wear Failure": (
       """Tool wear failure occurs when the cutting tool in the machine wears out due to continuous use, 
       leading to inefficient cutting and poor product quality. To reduce tool wear:
        <br>1. Use high-quality, wear-resistant tools.
        <br>2. Regularly inspect and replace tools.
        <br>3. Optimize cutting parameters to reduce wear.
        <br>4. Apply proper lubrication to reduce friction.
        <br>5. Implement a tool wear monitoring system.
        <br>6. Use coatings on tools to increase durability.
        <br>7. Avoid excessive cutting speeds.
        <br>8. Maintain optimal feed rates.
        <br>9. Ensure proper cooling during operations.
        <br>10. Train operators on best practices for tool maintenance."""
    ),
    "Heat Dissipation Failure": (
        """Heat dissipation failure happens when the machine cannot effectively dissipate heat,
          causing overheating and potential damage. To prevent this:
          <br>1. Ensure the cooling system is functioning properly.
          <br>2. Regularly clean and maintain cooling components.
          <br>3. Use high-quality coolant.
          <br>4. Monitor and control process temperatures.
          <br>5. Avoid excessive cutting speeds that generate heat.
          <br>6. Implement a thermal management system.
          <br>7. Use heat-resistant materials.
          <br>8. Maintain proper airflow around the machine.
          <br>9. Regularly check for blockages in cooling pathways.
          <br>10. Train operators on managing process temperatures."""
    ),
    "Power Failure": (
        """Power failure can result from unstable or insufficient power supply, leading to machine shutdowns or malfunctions. 
        To mitigate this:
        <br>1. Use a stable and reliable power source.
        <br>2. Install uninterruptible power supplies (UPS).
        <br>3. Regularly maintain electrical components.
        <br>4. Monitor power supply quality.
        <br>5. Ensure proper grounding of the machine.
        <br>6. Use surge protectors to prevent damage from power spikes.
        <br>7. Implement a power management system.
        <br>8. Avoid running multiple high-power machines simultaneously.
        <br>9. Regularly inspect power cables and connections.
        <br>10. Train operators on electrical safety and power management."""
    ),
    "Overstrain Failure": (
        """Overstrain failure occurs when the machine is subjected to loads beyond its capacity, causing mechanical failures.
        To avoid this:
        <br>1. Operate within recommended load limits.
        <br>2. Regularly calibrate and maintain the machine.
        <br>3. Monitor and control torque and speed.
        <br>4. Use overload protection devices.
        <br>5. Avoid abrupt changes in load.
        <br>6. Implement a load management system.
        <br>7. Train operators on machine capacity and limits.
        <br>8. Use high-quality, durable components.
        <br>9. Perform regular stress tests on the machine.
        <br>10. Ensure proper alignment and balance of moving parts."""
    )
}

# Ideal values for comparison in charts
ideal_values = [300, 310, 2000, 50, 150]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    product_type = data['type']
    air_temp = float(data['air_temperature'])
    process_temp = float(data['process_temperature'])
    rotational_speed = int(data['rotational_speed'])
    torque = float(data['torque'])
    tool_wear = int(data['tool_wear'])

    # Encoding categorical variables if necessary
    type_encoding = {'L': 0, 'M': 1, 'H': 2}
    product_type_encoded = type_encoding.get(product_type, 0)
    
    # Prepare the input data
    input_data = np.array([[product_type_encoded, air_temp, process_temp, rotational_speed, torque, tool_wear]])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    failure_type = failure_types.get(prediction, "Unknown Failure")
    suggestion = parameter_suggestions.get(prediction, "No suggestions available.")
    
    # Return the input and ideal values for visualization
    input_values = [air_temp, process_temp, rotational_speed, torque, tool_wear]

    return jsonify({'prediction': failure_type, 'suggestion': suggestion, 'input_values': input_values, 'ideal_values': ideal_values})

@app.route('/ai_analysis', methods=['POST'])
def ai_analysis():
    data = request.get_json()
    prediction = data['prediction']
    analysis = detailed_analysis.get(prediction, "No detailed analysis available for this failure type.")
    
    return jsonify({'analysis': analysis})

if __name__ == "__main__":
    app.run(debug=True)
